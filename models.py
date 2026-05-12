from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="admin")

   
    orders = relationship("Order", back_populates="user")


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(Text, nullable=False)


    orders = relationship("Order", back_populates="customer")
    notifications = relationship("Notification", back_populates="customer")



class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)

    services = relationship("Service", back_populates="category")


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    service_name = Column(String(100), nullable=False)
    price_per_kg = Column(Integer, nullable=False)
    estimated_days = Column(Integer, nullable=False)
    image_url = Column(String(255), nullable=True)

    category = relationship("Category", back_populates="services")
    orders = relationship("Order", back_populates="service")



class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    service_id = Column(Integer, ForeignKey("services.id"))
    weight = Column(Float, nullable=False)
    total_price = Column(Integer, nullable=False)
    status = Column(String(20), default="pending") 
    order_date = Column(String(50), nullable=False)

    user = relationship("User", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")
    service = relationship("Service", back_populates="orders")
   
    payment = relationship("Payment", back_populates="order", uselist=False)



class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True)
    payment_method = Column(String(50), nullable=False)
    amount_paid = Column(Integer, nullable=False)
    payment_status = Column(String(20), default="unpaid") 
    payment_date = Column(String(50), nullable=False)

    order = relationship("Order", back_populates="payment")



class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(100), nullable=False)
    amount = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False) 
    date = Column(String(50), nullable=False)


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    title = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    sent_at = Column(String(50), nullable=False)

    customer = relationship("Customer", back_populates="notifications")