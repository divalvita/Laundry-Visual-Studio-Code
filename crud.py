from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

import models
import schemas


# =====================================================
# USERS CRUD
# =====================================================

def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):

    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email sudah digunakan"
        )

    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):

    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    db.delete(user)
    db.commit()

    return {"message": "User berhasil dihapus"}


# =====================================================
# CUSTOMERS CRUD
# =====================================================

def get_customers(db: Session):
    return db.query(models.Customer).all()


def get_customer_by_id(db: Session, customer_id: int):
    return db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()


def create_customer(db: Session, customer: schemas.CustomerCreate):

    db_customer = models.Customer(
        name=customer.name,
        phone=customer.phone,
        address=customer.address
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


def update_customer(db: Session, customer_id: int, customer: schemas.CustomerCreate):

    db_customer = get_customer_by_id(db, customer_id)

    if not db_customer:
        raise HTTPException(
            status_code=404,
            detail="Customer tidak ditemukan"
        )

    db_customer.name = customer.name
    db_customer.phone = customer.phone
    db_customer.address = customer.address

    db.commit()
    db.refresh(db_customer)

    return db_customer


def delete_customer(db: Session, customer_id: int):

    customer = get_customer_by_id(db, customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer tidak ditemukan"
        )

    db.delete(customer)
    db.commit()

    return {"message": "Customer berhasil dihapus"}


# =====================================================
# CATEGORY CRUD
# =====================================================

def get_categories(db: Session):
    return db.query(models.Category).all()


def create_category(db: Session, category: schemas.CategoryCreate):

    db_category = models.Category(
        category_name=category.category_name,
        description=category.description
    )

    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


# =====================================================
# SERVICE CRUD
# =====================================================

def get_services(db: Session):
    return db.query(models.Service).all()


def get_service_by_id(db: Session, service_id: int):
    return db.query(models.Service).filter(
        models.Service.id == service_id
    ).first()


def create_service(db: Session, service: schemas.ServiceCreate):

    category = db.query(models.Category).filter(
        models.Category.id == service.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category tidak ditemukan"
        )

    db_service = models.Service(
        category_id=service.category_id,
        service_name=service.service_name,
        price_per_kg=service.price_per_kg,
        estimated_days=service.estimated_days,
        image_url=service.image_url
    )

    db.add(db_service)
    db.commit()
    db.refresh(db_service)

    return db_service


def update_service(db: Session, service_id: int, service: schemas.ServiceCreate):

    db_service = get_service_by_id(db, service_id)

    if not db_service:
        raise HTTPException(
            status_code=404,
            detail="Service tidak ditemukan"
        )

    db_service.category_id = service.category_id
    db_service.service_name = service.service_name
    db_service.price_per_kg = service.price_per_kg
    db_service.estimated_days = service.estimated_days
    db_service.image_url = service.image_url

    db.commit()
    db.refresh(db_service)

    return db_service


def delete_service(db: Session, service_id: int):

    service = get_service_by_id(db, service_id)

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service tidak ditemukan"
        )

    db.delete(service)
    db.commit()

    return {"message": "Service berhasil dihapus"}


# =====================================================
# ORDER CRUD + BUSINESS LOGIC
# =====================================================

def get_orders(db: Session):
    return db.query(models.Order).all()


def get_order_by_id(db: Session, order_id: int):
    return db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()


def create_order(
    db: Session,
    order: schemas.OrderCreate,
    current_user_id: int
):

    customer = db.query(models.Customer).filter(
        models.Customer.id == order.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer tidak ditemukan"
        )

    service = db.query(models.Service).filter(
        models.Service.id == order.service_id
    ).first()

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service tidak ditemukan"
        )

    # ==========================
    # HITUNG TOTAL OTOMATIS
    # ==========================

    total_price = order.weight * service.price_per_kg

    db_order = models.Order(
        user_id=current_user_id,
        customer_id=order.customer_id,
        service_id=order.service_id,
        weight=order.weight,
        total_price=int(total_price),
        status="pending",
        order_date=str(datetime.now())
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def update_order_status(
    db: Session,
    order_id: int,
    order_update: schemas.OrderUpdate
):

    db_order = get_order_by_id(db, order_id)

    if not db_order:
        raise HTTPException(
            status_code=404,
            detail="Order tidak ditemukan"
        )

    allowed_status = [
        "pending",
        "processing",
        "done",
        "taken"
    ]

    if order_update.status not in allowed_status:
        raise HTTPException(
            status_code=400,
            detail="Status tidak valid"
        )

    db_order.status = order_update.status

    db.commit()
    db.refresh(db_order)

    return db_order


def delete_order(db: Session, order_id: int):

    order = get_order_by_id(db, order_id)

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order tidak ditemukan"
        )

    db.delete(order)
    db.commit()

    return {"message": "Order berhasil dihapus"}


# =====================================================
# PAYMENT CRUD + BUSINESS LOGIC
# =====================================================

def get_payments(db: Session):
    return db.query(models.Payment).all()


def create_payment(db: Session, payment: schemas.PaymentCreate):

    order = db.query(models.Order).filter(
        models.Order.id == payment.order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order tidak ditemukan"
        )

    existing_payment = db.query(models.Payment).filter(
        models.Payment.order_id == payment.order_id
    ).first()

    if existing_payment:
        raise HTTPException(
            status_code=400,
            detail="Payment sudah ada"
        )

    # ==========================
    # VALIDASI PEMBAYARAN
    # ==========================

    if payment.amount_paid < order.total_price:
        payment_status = "unpaid"
    else:
        payment_status = "paid"

    db_payment = models.Payment(
        order_id=payment.order_id,
        payment_method=payment.payment_method,
        amount_paid=payment.amount_paid,
        payment_status=payment_status,
        payment_date=str(datetime.now())
    )

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment


# =====================================================
# EXPENSE CRUD
# =====================================================

def get_expenses(db: Session):
    return db.query(models.Expense).all()


def create_expense(db: Session, expense: schemas.ExpenseCreate):

    db_expense = models.Expense(
        item_name=expense.item_name,
        amount=expense.amount,
        category=expense.category,
        date=expense.date
    )

    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense


# =====================================================
# NOTIFICATION CRUD
# =====================================================

def get_notifications(db: Session):
    return db.query(models.Notification).all()


def create_notification(
    db: Session,
    notification: schemas.NotificationCreate
):

    customer = db.query(models.Customer).filter(
        models.Customer.id == notification.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer tidak ditemukan"
        )

    db_notification = models.Notification(
        customer_id=notification.customer_id,
        title=notification.title,
        message=notification.message,
        sent_at=str(datetime.now())
    )

    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)

    return db_notification