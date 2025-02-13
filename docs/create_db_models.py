# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime

Base = declarative_base()

# Define the models

class Client(Base):
    """
    description: Table to store client information.
    """
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=False)
    whatsapp_number = Column(String, nullable=True)  # Client WhatsApp number
    registration_date = Column(DateTime, default=datetime.datetime.now)


class Interaction(Base):
    """
    description: Stores interactions between the business and clients.
    """
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    datetime = Column(DateTime, default=datetime.datetime.now)
    type = Column(String, nullable=False)  # e.g., "call", "email", "whatsapp"
    notes = Column(Text, nullable=True)


class WhatsappMessage(Base):
    """
    description: Stores WhatsApp messages.
    """
    __tablename__ = 'whatsapp_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    datetime = Column(DateTime, default=datetime.datetime.now)
    direction = Column(String, nullable=False)  # "sent" or "received"
    message_content = Column(Text, nullable=False)


class Task(Base):
    """
    description: Stores tasks assigned for interacting with clients.
    """
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    due_date = Column(DateTime, nullable=False)
    description = Column(Text, nullable=False)
    completed = Column(Boolean, default=False)


class Product(Base):
    """
    description: Table to store products that can be sold to clients.
    """
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Integer, nullable=False)  # Price in cents to avoid using decimals


class Order(Base):
    """
    description: Stores client orders.
    """
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.now)


class OrderDetail(Base):
    """
    description: Contains details of each product in a client order.
    """
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)


class Feedback(Base):
    """
    description: Stores feedback from clients.
    """
    __tablename__ = 'feedbacks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    datetime = Column(DateTime, default=datetime.datetime.now)
    comments = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)  # Rating from 1 to 5


class Address(Base):
    """
    description: Stores addresses of clients.
    """
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False)


class CustomerSupport(Base):
    """
    description: Records interactions with customer support.
    """
    __tablename__ = 'customer_support'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    issue_description = Column(Text, nullable=False)
    resolved = Column(Boolean, default=False)
    resolution_date = Column(DateTime, nullable=True)


class Appointment(Base):
    """
    description: Stores appointments with clients.
    """
    __tablename__ = 'appointments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    datetime = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    purpose = Column(Text, nullable=False)


class Chat(Base):
    """
    description: Stores chat logs of interactions with clients.
    """
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    datetime = Column(DateTime, default=datetime.datetime.now)
    chat_content = Column(Text, nullable=False)

# Create the database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Sample data for each table

# Clients
clients = [
    Client(name='Alice', email='alice@example.com', phone='1234567890', whatsapp_number='+1234567890'),
    Client(name='Bob', email='bob@example.com', phone='0987654321', whatsapp_number='+10987654321'),
    # Add more client rows as needed
]

# Interactions
interactions = [
    Interaction(client_id=1, type='whatsapp', notes='Discussed project requirements'),
    Interaction(client_id=2, type='email', notes='Sent a follow-up email'),
    # Add more interaction rows as needed
]

# WhatsappMessages
whatsapp_messages = [
    WhatsappMessage(client_id=1, direction='received', message_content='Thanks for the detailed plan!'),
    WhatsappMessage(client_id=2, direction='sent', message_content='Let me know your thoughts.'),
    # Add more message rows as needed
]

# Tasks
tasks = [
    Task(client_id=1, due_date=datetime.datetime(2023, 12, 31), description='Send end of year report'),
    Task(client_id=2, due_date=datetime.datetime(2023, 11, 15), description='Follow-up meeting'),
    # Add more task rows as needed
]

# Products
products = [
    Product(name='Product A', description='High-quality product A', price=1000),
    Product(name='Product B', description='Affordable product B', price=500),
    # Add more product rows as needed
]

# Orders
orders = [
    Order(client_id=1, order_date=datetime.datetime(2023, 10, 10)),
    Order(client_id=2, order_date=datetime.datetime(2023, 9, 20)),
    # Add more order rows as needed
]

# OrderDetails
order_details = [
    OrderDetail(order_id=1, product_id=1, quantity=2),
    OrderDetail(order_id=2, product_id=2, quantity=1),
    # Add more order detail rows as needed
]

# Feedbacks
feedbacks = [
    Feedback(client_id=1, comments='Great service!', rating=5),
    Feedback(client_id=2, comments='Could be better', rating=3),
    # Add more feedback rows as needed
]

# Addresses
addresses = [
    Address(client_id=1, street='123 Main St', city='Anytown', state='Anystate', zip_code='12345', country='Anyland'),
    Address(client_id=2, street='456 Elm St', city='Othertown', state='Otherstate', zip_code='67890', country='Otherland'),
    # Add more address rows as needed
]

# CustomerSupport
customer_support = [
    CustomerSupport(client_id=1, issue_description='Login issue', resolved=True, resolution_date=datetime.datetime(2023, 9, 1)),
    CustomerSupport(client_id=2, issue_description='Payment not processed', resolved=False),
    # Add more customer support rows as needed
]

# Appointments
appointments = [
    Appointment(client_id=1, datetime=datetime.datetime(2023, 11, 5, 14, 0), location='Client Office', purpose='Project Kick-off'),
    Appointment(client_id=2, datetime=datetime.datetime(2023, 10, 18, 9, 30), location='Video Call', purpose='Monthly Review'),
    # Add more appointment rows as needed
]

# Chats
chats = [
    Chat(client_id=1, chat_content='Chat about project milestones.'),
    Chat(client_id=2, chat_content='Discuss payment terms.'),
    # Add more chat rows as needed
]

# Add all records to the session
session.add_all(clients + interactions + whatsapp_messages + tasks + products + orders +
                order_details + feedbacks + addresses + customer_support + appointments + chats)

# Commit the transaction
session.commit()

# Close the session
session.close()
