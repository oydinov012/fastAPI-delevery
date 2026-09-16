
from turtle import back

from annotated_types import T
from fastapi.background import P
from sqlalchemy import Column ,Text , ForeignKey , Integer , Boolean , String, null
from database import Base, Session
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType





class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True )
    username = Column(String(40),unique=True)
    email = Column(String(40),unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active= Column(Boolean, default=False)
    orders = relationship("Order", back_populates='user')


class Order(Base):
    ORDER_STATUS = (
        ("PENDING","pending"),
        ("IN_TRANZIT","in_tranzit"),
        ("DELEVIRED","delevired")
    )
    __tablename__ = "orders"
    id = Column(Integer,primary_key=True)
    quantity = Column(Integer,nullable=True)
    order_statuses = Column(ChoiceType(choices=ORDER_STATUS),default="PENDING")
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship("User",back_populates="orders")
    product = relationship("Product",back_populates="orders")
    

    def __repr__(self):
        return f">> Order {self.id} -- Product {self.product}"


class Product(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Integer)

    def __repr__(self):
        return f">> Product {self.name}"