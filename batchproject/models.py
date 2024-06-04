from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(80), nullable=False)

class Policy(db.Model):
    __tablename__ = 'policies'
    id = db.Column(db.String, primary_key=True)
    amount_insured = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    inception_date = db.Column(db.DateTime, nullable=False)
    installment_payment = db.Column(db.Boolean, nullable=False)
    client_id = db.Column(db.String, db.ForeignKey('clients.id'), nullable=False)
