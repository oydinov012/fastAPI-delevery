from sqlalchemy import Column ,Text , ForeignKey , Integer , Boolean , String
from database import Base
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


    def __repr__(self):
        return f"user >> {self.username}"

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
    user_id = Column(Integer,ForeignKey('users.id'))
    user = relationship("User",back_populates="orders")

    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product",back_populates="orders")

    def __repr__(self):
        return f">> Order {self.id} -- Product {self.product}"


class Product(Base):

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    price = Column(Integer)
    orders = relationship("Order", back_populates='product')

    

    def __repr__(self):
        return f">> Product -->  {self.name}"