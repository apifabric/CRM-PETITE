# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 17, 2024 18:01:02
# Database: sqlite:////tmp/tmp.i0TH7nVke1/CRM-PETITE/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Client(SAFRSBaseX, Base):
    """
    description: Table to store client information.
    """
    __tablename__ = 'clients'
    _s_collection_name = 'Client'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String, nullable=False)
    whatsapp_number = Column(String)
    registration_date = Column(DateTime)

    # parent relationships (access parent)

    # child relationships (access children)
    AddressList : Mapped[List["Address"]] = relationship(back_populates="client")
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="client")
    ChatList : Mapped[List["Chat"]] = relationship(back_populates="client")
    CustomerSupportList : Mapped[List["CustomerSupport"]] = relationship(back_populates="client")
    FeedbackList : Mapped[List["Feedback"]] = relationship(back_populates="client")
    InteractionList : Mapped[List["Interaction"]] = relationship(back_populates="client")
    OrderList : Mapped[List["Order"]] = relationship(back_populates="client")
    TaskList : Mapped[List["Task"]] = relationship(back_populates="client")
    WhatsappMessageList : Mapped[List["WhatsappMessage"]] = relationship(back_populates="client")



class Product(SAFRSBaseX, Base):
    """
    description: Table to store products that can be sold to clients.
    """
    __tablename__ = 'products'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Integer, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderDetailList : Mapped[List["OrderDetail"]] = relationship(back_populates="product")



class Address(SAFRSBaseX, Base):
    """
    description: Stores addresses of clients.
    """
    __tablename__ = 'addresses'
    _s_collection_name = 'Address'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    country = Column(String, nullable=False)

    # parent relationships (access parent)
    client : Mapped["Client"] = relationship(back_populates=("AddressList"))

    # child relationships (access children)



class Appointment(SAFRSBaseX, Base):
    """
    description: Stores appointments with clients.
    """
    __tablename__ = 'appointments'
    _s_collection_name = 'Appointment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    datetime = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    purpose = Column(Text, nullable=False)

    # parent relationships (access parent)
    client : Mapped["Client"] = relationship(back_populates=("AppointmentList"))

    # child relationships (access children)



class Chat(SAFRSBaseX, Base):
    """
    description: Stores chat logs of interactions with clients.
    """
    __tablename__ = 'chats'
    _s_collection_name = 'Chat'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    datetime = Column(DateTime)
    chat_content = Column(Text, nullable=False)

    # parent relationships (access parent)
    client : Mapped["Client"] = relationship(back_populates=("ChatList"))

    # child relationships (access children)



class CustomerSupport(SAFRSBaseX, Base):
    """
    description: Records interactions with customer support.
    """
    __tablename__ = 'customer_support'
    _s_collection_name = 'CustomerSupport'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    issue_description = Column(Text, nullable=False)
    resolved = Column(Boolean)
    resolution_date = Column(DateTime)

    # parent relationships (access parent)
    client : Mapped["Client"] = relationship(back_populates=("CustomerSupportList"))

    # child relationships (access children)



class Feedback(SAFRSBaseX, Base):
    """
    description: Stores feedback from clients.
    """
    __tablename__ = 'feedbacks'
    _s_collection_name = 'Feedback'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    datetime = Column(DateTime)
    comments = Column(Text)
    rating = Column(Integer, nullable=False)

    # parent relationships (access parent)
    client : Mapped["Client"] = relationship(back_populates=("FeedbackList"))

    # child relationships (access children)



class Interaction(SAFRSBaseX, Base):
    """
    description: Stores interactions between the business and clients.
    """
    __tablename__ = 'interactions'
    _s_collection_name = 'Interaction'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    datetime = Column(DateTime)
    type = Column(String, nullable=False)
    notes = Column(Text)

    # parent relationships (access parent)
    client : Mapped["Client"] = relationship(back_populates=("InteractionList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Stores client orders.
    """
    __tablename__ = 'orders'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    order_date = Column(DateTime)

    # parent relationships (access parent)
    client : Mapped["Client"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderDetailList : Mapped[List["OrderDetail"]] = relationship(back_populates="order")



class Task(SAFRSBaseX, Base):
    """
    description: Stores tasks assigned for interacting with clients.
    """
    __tablename__ = 'tasks'
    _s_collection_name = 'Task'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    due_date = Column(DateTime, nullable=False)
    description = Column(Text, nullable=False)
    completed = Column(Boolean)

    # parent relationships (access parent)
    client : Mapped["Client"] = relationship(back_populates=("TaskList"))

    # child relationships (access children)



class WhatsappMessage(SAFRSBaseX, Base):
    """
    description: Stores WhatsApp messages.
    """
    __tablename__ = 'whatsapp_messages'
    _s_collection_name = 'WhatsappMessage'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    client_id = Column(ForeignKey('clients.id'), nullable=False)
    datetime = Column(DateTime)
    direction = Column(String, nullable=False)
    message_content = Column(Text, nullable=False)

    # parent relationships (access parent)
    client : Mapped["Client"] = relationship(back_populates=("WhatsappMessageList"))

    # child relationships (access children)



class OrderDetail(SAFRSBaseX, Base):
    """
    description: Contains details of each product in a client order.
    """
    __tablename__ = 'order_details'
    _s_collection_name = 'OrderDetail'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('orders.id'), nullable=False)
    product_id = Column(ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderDetailList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderDetailList"))

    # child relationships (access children)
