from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from typing import List


# =========================================
# DASHBOARD SCHEMA
# =========================================
class WeeklyIncome(BaseModel):
    label: str
    amount: int

class DashboardStats(BaseModel):
    active_orders:  int
    done_orders:    int
    taken_orders:   int
    total_orders:   int
    total_income:   int
    total_expense:  int
    total_profit:   int
    weekly_income:  List[WeeklyIncome]
    monthly_income: List[WeeklyIncome]

    
# =========================
# USERS SCHEMA
# =========================

class UserBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    role: Optional[str] = "admin"


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str
# =========================
# CUSTOMERS SCHEMA
# =========================

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    phone: str = Field(..., min_length=10, max_length=20)
    address: str = Field(..., min_length=5)


class CustomerCreate(CustomerBase):
    pass


class CustomerOut(CustomerBase):
    id: int

    class Config:
        orm_mode = True


# =========================
# CATEGORY SCHEMA
# =========================

class CategoryBase(BaseModel):
    category_name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryOut(CategoryBase):
    id: int

    class Config:
        orm_mode = True


# =========================
# SERVICE SCHEMA
# =========================

class ServiceBase(BaseModel):
    service_name: str = Field(..., min_length=3, max_length=100)
    price_per_kg: int = Field(..., gt=0)
    estimated_days: int = Field(..., gt=0)
    image_url: Optional[str] = None


class ServiceCreate(ServiceBase):
    pass


class ServiceOut(ServiceBase):
    id: int

    class Config:
        orm_mode = True


# =========================
# ORDER SCHEMA
# =========================

class OrderBase(BaseModel):
    customer_id: int
    service_id: int
    weight: float = Field(..., gt=0)


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: str = Field(...)


class OrderOut(BaseModel):
    id: int
    user_id: int
    customer_id: int
    service_id: int
    weight: float
    total_price: int
    status: str
    order_date: str

    class Config:
        orm_mode = True


# =========================
# PAYMENT SCHEMA
# =========================

class PaymentBase(BaseModel):
    order_id: int
    payment_method: str = Field(..., min_length=3)
    amount_paid: int = Field(..., ge=0)


class PaymentCreate(PaymentBase):
    pass


class PaymentOut(BaseModel):
    id: int
    order_id: int
    payment_method: str
    amount_paid: int
    payment_status: str
    payment_date: str

    class Config:
        orm_mode = True


# =========================
# EXPENSE SCHEMA
# =========================

class ExpenseBase(BaseModel):
    item_name: str = Field(..., min_length=3, max_length=100)
    amount: int = Field(..., gt=0)
    category: str = Field(..., min_length=3, max_length=50)
    date: str


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseOut(ExpenseBase):
    id: int

    class Config:
        orm_mode = True


# =========================
# NOTIFICATION SCHEMA
# =========================

class NotificationBase(BaseModel):
    customer_id: int
    title: str = Field(..., min_length=3, max_length=100)
    message: str = Field(..., min_length=5)


class NotificationCreate(NotificationBase):
    pass


class NotificationOut(NotificationBase):
    id: int
    sent_at: str

    class Config:
        orm_mode = True