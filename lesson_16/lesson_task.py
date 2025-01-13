# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Enum, func
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError
from datetime import date
from enum import Enum as PyEnum

# Создаем базовый класс для декларативного определения моделей
Base = declarative_base()


# Определяем перечисление для типа недвижимости
class PropertyType(PyEnum):
    RESIDENTIAL = "residential"  # Жилая недвижимость
    COMMERCIAL = "commercial"  # Коммерческая недвижимость


# Определяем перечисление для статуса договора аренды
class LeaseStatus(PyEnum):
    ACTIVE = "active"  # Активный договор
    COMPLETED = "completed"  # Завершенный договор


# Модель для сущности "Пользователь"
class User(Base):
    __tablename__ = 'users'  # Название таблицы в базе данных
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    name = Column(String, nullable=False)  # Имя пользователя
    email = Column(String, unique=True, nullable=False)  # Электронная почта (уникальная)
    leases = relationship("Lease", back_populates="tenant")  # Связь с договорами аренды


# Модель для сущности "Объект недвижимости"
class Property(Base):
    __tablename__ = 'properties'  # Название таблицы
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    address = Column(String, nullable=False)  # Адрес недвижимости
    type = Column(Enum(PropertyType), nullable=False)  # Тип недвижимости (жилая/коммерческая)
    rent_price = Column(Float, nullable=False)  # Стоимость аренды
    leases = relationship("Lease", back_populates="property")  # Связь с договорами аренды


# Модель для сущности "Договор аренды"
class Lease(Base):
    __tablename__ = 'leases'  # Название таблицы
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    start_date = Column(Date, nullable=False)  # Дата начала аренды
    end_date = Column(Date, nullable=False)  # Дата окончания аренды
    status = Column(Enum(LeaseStatus), nullable=False, default=LeaseStatus.ACTIVE)  # Статус договора
    tenant_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Связь с арендатором
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)  # Связь с объектом недвижимости
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=True)  # Связь с агентом (опционально)
    tenant = relationship("User", back_populates="leases")  # Связь с пользователем
    property = relationship("Property", back_populates="leases")  # Связь с объектом недвижимости
    agent = relationship("Agent", back_populates="leases")  # Связь с агентом
    payments = relationship("Payment", back_populates="lease")  # Связь с платежами


# Модель для сущности "Платёж"
class Payment(Base):
    __tablename__ = 'payments'  # Название таблицы
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    amount = Column(Float, nullable=False)  # Сумма платежа
    payment_date = Column(Date, nullable=False)  # Дата платежа
    lease_id = Column(Integer, ForeignKey('leases.id'), nullable=False)  # Связь с договором аренды
    lease = relationship("Lease", back_populates="payments")  # Связь с договором


# Модель для сущности "Агент"
class Agent(Base):
    __tablename__ = 'agents'  # Название таблицы
    id = Column(Integer, primary_key=True)  # Уникальный идентификатор
    name = Column(String, nullable=False)  # Имя агента
    commission_rate = Column(Float, nullable=False)  # Процент комиссии
    leases = relationship("Lease", back_populates="agent")  # Связь с договорами аренды


# Создаем подключение к базе данных SQLite
engine = create_engine('sqlite:///real_estate.db')

# Очищаем базу данных перед началом работы (удаляем все таблицы)
Base.metadata.drop_all(engine)

# Создаем все таблицы в базе данных
Base.metadata.create_all(engine)

# Создаем фабрику сессий
Session = sessionmaker(bind=engine)

# Глобальная сессия (если нужна)
session = Session()


# Функция для добавления пользователя с проверкой на существование
def add_user_if_not_exists(name, email):
    # Используем глобальную сессию
    existing_user = session.query(User).filter_by(email=email).first()
    if existing_user:
        print(f"User with email {email} already exists.")
        return existing_user
    else:
        # Создаем нового пользователя
        user = User(name=name, email=email)
        session.add(user)
        session.commit()
        print(f"User {name} added successfully.")
        return user


# Добавляем пользователей
add_user_if_not_exists("John Doe", "john@example.com")
add_user_if_not_exists("Jane Smith", "jane@example.com")

# Добавляем объекты недвижимости
property1 = Property(address="123 Main St", type=PropertyType.RESIDENTIAL, rent_price=1000)
property2 = Property(address="456 Elm St", type=PropertyType.COMMERCIAL, rent_price=2000)
session.add_all([property1, property2])
session.commit()

# Добавляем договоры аренды
user1 = session.query(User).filter_by(email="john@example.com").first()
user2 = session.query(User).filter_by(email="jane@example.com").first()

lease1 = Lease(start_date=date(2023, 10, 1),
               end_date=date(2024, 9, 30), tenant=user1, property=property1)
lease2 = Lease(start_date=date(2023, 11, 1),
               end_date=date(2024, 10, 31), tenant=user2, property=property2)
session.add_all([lease1, lease2])
session.commit()

# Добавляем агента
agent1 = Agent(name="Alice Brown", commission_rate=0.1)
session.add(agent1)
session.commit()


# Функция для внесения платежа
def make_payment(lease_id, amount, payment_date):
    # Используем глобальную сессию
    lease = session.get(Lease, lease_id)
    if not lease:
        raise ValueError("Lease not found")

    # Создаем новый платеж
    payment = Payment(amount=amount, payment_date=payment_date, lease=lease)
    session.add(payment)

    # Если это первый платеж, активируем договор
    if not lease.payments:
        lease.status = LeaseStatus.ACTIVE

    # Сохраняем изменения в базе данных
    session.commit()
    print(f"Payment of {amount} made for lease {lease_id}.")


# Функция для завершения договора аренды
def complete_lease(lease_id):
    # Используем глобальную сессию
    lease = session.get(Lease, lease_id)
    if not lease:
        raise ValueError("Lease not found")

    # Меняем статус договора на "завершен"
    lease.status = LeaseStatus.COMPLETED
    session.commit()
    print(f"Lease {lease_id} marked as completed.")


# Функция для поиска пользователей без платежей
def find_users_without_payments():
    # Используем глобальную сессию
    users_without_payments = session.query(User).outerjoin(Lease).outerjoin(Payment).filter(Payment.id.is_(None)).all()
    for user in users_without_payments:
        print(f"User without payments: {user.name}")


# Функция для поиска объектов недвижимости, арендованных более 3 раз
def find_properties_rented_more_than_3_times():
    # Используем глобальную сессию
    properties_rented_more_than_3_times = session.query(Property).join(Lease).group_by(Property.id).having(
        func.count(Lease.id) > 3).all()
    for property in properties_rented_more_than_3_times:
        print(f"Property rented more than 3 times: {property.address}")


# Функция для создания договора и внесения первого платежа в одной транзакции
def create_lease_and_make_payment(user_id, property_id, start_date, end_date, amount, payment_date):
    try:
        # Используем глобальную сессию
        lease = Lease(start_date=start_date, end_date=end_date, tenant_id=user_id, property_id=property_id)
        session.add(lease)
        session.flush()  # Сохраняем договор, чтобы получить его ID

        # Создаем платеж
        payment = Payment(amount=amount, payment_date=payment_date, lease_id=lease.id)
        session.add(payment)

        # Сохраняем изменения в базе данных
        session.commit()
        print(f"Lease created and payment made successfully.")
    except IntegrityError:
        # В случае ошибки откатываем транзакцию
        session.rollback()
        raise


# Функция для расчета комиссии агента
def calculate_agent_commission(lease_id):
    # Используем глобальную сессию
    lease = session.get(Lease, lease_id)
    if not lease or not lease.agent:
        return 0

    # Считаем общую сумму платежей по договору
    total_payments = sum(payment.amount for payment in lease.payments)

    # Рассчитываем комиссию агента
    agent_commission = total_payments * lease.agent.commission_rate
    print(f"Agent commission for lease {lease_id}: {agent_commission}")
    return agent_commission


# Пример использования функций
make_payment(lease1.id, 1000, date(2023, 10, 1))
complete_lease(lease1.id)
create_lease_and_make_payment(user1.id, property1.id, date(2023, 12, 1),
                              date(2024, 11, 30), 1000, date(2023, 12, 1))
agent_commission = calculate_agent_commission(lease1.id)

# Выполняем сложные запросы
find_users_without_payments()
find_properties_rented_more_than_3_times()

# Добавляем пустую строку в конце файла для соответствия PEP 8
