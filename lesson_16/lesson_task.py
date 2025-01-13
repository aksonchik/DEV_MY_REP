# Импорт необходимых библиотек
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import date
from enum import Enum as PyEnum

# Создание Flask-приложения
app = Flask(__name__)

# Настройки базы данных
engine = create_engine('sqlite:///real_estate.db')
Session = sessionmaker(bind=engine)
session = Session()

# Базовый класс для декларативного определения моделей
Base = declarative_base()


# Перечисления и модели

# Перечисление для типа недвижимости
class PropertyType(PyEnum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"


# Перечисление для статуса договора аренды
class LeaseStatus(PyEnum):
    ACTIVE = "active"
    COMPLETED = "completed"


# Модель для сущности "Пользователь"
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)  # Первичный ключ
    name = Column(String, nullable=False)  # Имя пользователя (обязательное поле)
    email = Column(String, unique=True, nullable=False)  # Электронная почта (уникальная и обязательная)
    leases = relationship("Lease", back_populates="tenant")  # Связь с договорами аренды (один ко многим)


# Модель для сущности "Объект недвижимости"
class Property(Base):
    __tablename__ = 'properties'
    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)  # Адрес недвижимости (обязательное поле)
    type = Column(Enum(PropertyType), nullable=False)  # Тип недвижимости
    rent_price = Column(Float, nullable=False)  # Стоимость аренды (обязательное поле)
    leases = relationship("Lease", back_populates="property")  # Связь с договорами аренды (один ко многим)


# Модель для сущности "Договор аренды"
class Lease(Base):
    __tablename__ = 'leases'
    id = Column(Integer, primary_key=True)
    start_date = Column(Date, nullable=False)  # Дата начала аренды (обязательное поле)
    end_date = Column(Date, nullable=False)  # Дата окончания аренды (обязательное поле)
    status = Column(Enum(LeaseStatus), nullable=False, default=LeaseStatus.ACTIVE)  # Статус договора
    tenant_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Связь с арендатором (внешний ключ)
    property_id = Column(Integer, ForeignKey('properties.id'), nullable=False)  # с объектом недвижимости (внешний ключ)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=True)  # Связь с агентом (опционально)
    tenant = relationship("User", back_populates="leases")  # Связь с арендатором
    property = relationship("Property", back_populates="leases")  # Связь с объектом недвижимости
    agent = relationship("Agent", back_populates="leases")  # Связь с агентом
    payments = relationship("Payment", back_populates="lease")  # Связь с платежами (один ко многим)


# Модель для сущности "Платёж"
class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True)
    amount = Column(Float, nullable=False)  # Сумма платежа (обязательное поле)
    payment_date = Column(Date, nullable=False)  # Дата платежа (обязательное поле)
    lease_id = Column(Integer, ForeignKey('leases.id'), nullable=False)  # Связь с договором аренды (внешний ключ)
    lease = relationship("Lease", back_populates="payments")  # Связь с договором аренды


# Модель для сущности "Агент"
class Agent(Base):
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)  # Имя агента (обязательное поле)
    commission_rate = Column(Float, nullable=False)  # Процент комиссии (обязательное поле)
    leases = relationship("Lease", back_populates="agent")  # Связь с договорами аренды (один ко многим)


# Маршруты API

# Получить список всех пользователей
@app.route('/users', methods=['GET'])
def get_users():
    users = session.query(User).all()  # Запрос всех пользователей из базы данных
    return jsonify([{'id': user.id, 'name': user.name, 'email': user.email} for user in users])  # Возврат JSON-ответа


# Добавить нового пользователя
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(name=data['name'], email=data['email'])  # Создание нового пользователя
    session.add(new_user)
    session.commit()
    return jsonify({'id': new_user.id, 'name': new_user.name, 'email': new_user.email}), 201


# Получить список всех объектов недвижимости
@app.route('/properties', methods=['GET'])
def get_properties():
    properties = session.query(Property).all()
    return jsonify(
        [{'id': prop.id, 'address': prop.address, 'type': prop.type.value, 'rent_price': prop.rent_price} for prop in
         properties])


# Добавить новый объект недвижимости
@app.route('/properties', methods=['POST'])
def add_property():
    data = request.json
    new_property = Property(address=data['address'], type=PropertyType(data['type']),
                            rent_price=data['rent_price'])  # Создание нового объекта недвижимости
    session.add(new_property)
    session.commit()
    return jsonify({'id': new_property.id, 'address': new_property.address, 'type': new_property.type.value,
                    'rent_price': new_property.rent_price}), 201


# Получить список всех договоров аренды
@app.route('/leases', methods=['GET'])
def get_leases():
    leases = session.query(Lease).all()
    return jsonify([{'id': lease.id, 'start_date': lease.start_date.isoformat(), 'end_date': lease.end_date.isoformat(),
                     'status': lease.status.value, 'tenant_id': lease.tenant_id, 'property_id': lease.property_id,
                     'agent_id': lease.agent_id} for lease in leases])


# Добавить новый договор аренды
@app.route('/leases', methods=['POST'])
def add_lease():
    data = request.json
    new_lease = Lease(start_date=date.fromisoformat(data['start_date']), end_date=date.fromisoformat(data['end_date']),
                      tenant_id=data['tenant_id'], property_id=data['property_id'],
                      agent_id=data.get('agent_id'))
    session.add(new_lease)
    session.commit()
    return jsonify(
        {'id': new_lease.id, 'start_date': new_lease.start_date.isoformat(), 'end_date': new_lease.end_date.isoformat(),
         'status': new_lease.status.value, 'tenant_id': new_lease.tenant_id, 'property_id': new_lease.property_id,
         'agent_id': new_lease.agent_id}), 201


# Добавить новый платёж
@app.route('/payments', methods=['POST'])
def add_payment():
    data = request.json
    new_payment = Payment(amount=data['amount'], payment_date=date.fromisoformat(data['payment_date']),
                          lease_id=data['lease_id'])  # Создание нового платежа
    session.add(new_payment)
    session.commit()
    return jsonify(
        {'id': new_payment.id, 'amount': new_payment.amount, 'payment_date': new_payment.payment_date.isoformat(),
         'lease_id': new_payment.lease_id}), 201


# Получить список всех агентов
@app.route('/agents', methods=['GET'])
def get_agents():
    agents = session.query(Agent).all()
    return jsonify([{'id': agent.id, 'name': agent.name, 'commission_rate': agent.commission_rate} for agent in
                    agents])


# Добавить нового агента
@app.route('/agents', methods=['POST'])
def add_agent():
    data = request.json
    new_agent = Agent(name=data['name'], commission_rate=data['commission_rate'])
    session.add(new_agent)
    session.commit()
    return jsonify({'id': new_agent.id, 'name': new_agent.name, 'commission_rate': new_agent.commission_rate}), 201


# Запуск Flask
if __name__ == '__main__':
    app.run(debug=True)
