from .db import Reflected, Base
#from dataclasses import dataclass

# if we use e.g. DeferredReflection or specify classes explicitely

#@dataclass
class Customers(Reflected, Base):
    __tablename__ = "customers"

class Employees(Reflected, Base):
    __tablename__ = "employees"

class Offices(Reflected, Base):
    __tablename__ = "offices"
    
class OrderDetails(Reflected, Base):
    __tablename__ = "orderdetails"
    
class Orders(Reflected, Base):
    __tablename__ = "orders"
    
class Payments(Reflected, Base):
    __tablename__ = "payments"
    
class ProductLines(Reflected, Base):
    __tablename__ = "productlines"
   
class Products(Reflected, Base):
    __tablename__ = "products"

#@dataclass
class Countries(Reflected, Base):
    __tablename__ = "countries"

class Cities(Reflected, Base):
    __tablename__ = "cities"
