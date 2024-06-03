import requests
from sqlalchemy import create_engine, Column, String, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from uuid import UUID

DB_url = "postgresql://gaguirre:gaguirre@localhost/InsuranceDB"

# Define the SQLAlchemy model 
Base =  declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    role = Column(String)

class Policy(Base):
    __tablename__ = 'policies'
    id = Column(String, primary_key=True)
    amount_insured = Column(Float)
    email = Column(String)
    inception_date = Column(DateTime)
    installment_payment = Column(Boolean)
    client_id = Column(String)

# Crear la base de datos y las tablas
engine = create_engine(DB_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Leer los datos de las URLs
clients_url = "https://run.mocky.io/v3/532e77dc-2e2d-4a0c-91fd-5ea92ff5d615"
policies_url = "https://run.mocky.io/v3/289c72a0-8190-4a15-9a15-4118dc2fbde6"

clients_response = requests.get(clients_url)
policies_response = requests.get(policies_url)

clients_data = clients_response.json()
policies_data = policies_response.json()

# Insertar los datos en la base de datos
for client in clients_data:
    new_client = Client(id=client['id'], name=client['name'], email=client['email'], role=client['role'])
    session.add(new_client)

for policy in policies_data:
    new_policy = Policy(
        id=policy['id'],
        amount_insured=policy['amountInsured'],
        email=policy['email'],
        inception_date=policy['inceptionDate'],
        installment_payment=policy['installmentPayment'],
        client_id=policy['clientId']
    )
    session.add(new_policy)

session.commit()