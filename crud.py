from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta
from sqlalchemy import func

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

def update_user(
    db: Session,
    user_id: int,
    user: schemas.UserUpdate
):

    db_user = get_user_by_id(db, user_id)

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    db_user.name = user.name
    db_user.email = user.email
    db_user.role = user.role

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
def update_category(
    db: Session,
    category_id: int,
    category: schemas.CategoryCreate
):

    db_category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()

    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Category tidak ditemukan"
        )

    db_category.category_name = category.category_name
    db_category.description = category.description

    db.commit()
    db.refresh(db_category)

    return db_category
def delete_category(
    db: Session,
    category_id: int
):

    db_category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()

    if not db_category:
        raise HTTPException(
            status_code=404,
            detail="Category tidak ditemukan"
        )

    db.delete(db_category)
    db.commit()

    return {
        "message": "Category berhasil dihapus"
    }


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

    db_service = models.Service(
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
        status="processing", 
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


def update_payment(
    db: Session,
    payment_id: int,
    payment: schemas.PaymentCreate
):

    db_payment = db.query(models.Payment).filter(
        models.Payment.id == payment_id
    ).first()

    if not db_payment:
        raise HTTPException(
            status_code=404,
            detail="Payment tidak ditemukan"
        )

    order = db.query(models.Order).filter(
        models.Order.id == payment.order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order tidak ditemukan"
        )

    if payment.amount_paid < order.total_price:
        payment_status = "unpaid"
    else:
        payment_status = "paid"

    db_payment.order_id = payment.order_id
    db_payment.payment_method = payment.payment_method
    db_payment.amount_paid = payment.amount_paid
    db_payment.payment_status = payment_status

    db.commit()
    db.refresh(db_payment)

    return db_payment


def delete_payment(
    db: Session,
    payment_id: int
):

    db_payment = db.query(models.Payment).filter(
        models.Payment.id == payment_id
    ).first()

    if not db_payment:
        raise HTTPException(
            status_code=404,
            detail="Payment tidak ditemukan"
        )

    db.delete(db_payment)
    db.commit()

    return {
        "message": "Payment berhasil dihapus"
    }


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

def update_expense(
    db: Session,
    expense_id: int,
    expense: schemas.ExpenseCreate
):

    db_expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if not db_expense:
        raise HTTPException(
            status_code=404,
            detail="Expense tidak ditemukan"
        )

    db_expense.item_name = expense.item_name
    db_expense.amount = expense.amount
    db_expense.category = expense.category
    db_expense.date = expense.date

    db.commit()
    db.refresh(db_expense)

    return db_expense


def delete_expense(
    db: Session,
    expense_id: int
):

    db_expense = db.query(models.Expense).filter(
        models.Expense.id == expense_id
    ).first()

    if not db_expense:
        raise HTTPException(
            status_code=404,
            detail="Expense tidak ditemukan"
        )

    db.delete(db_expense)
    db.commit()

    return {
        "message": "Expense berhasil dihapus"
    }



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

def update_notification(
    db: Session,
    notification_id: int,
    notification: schemas.NotificationCreate
):

    db_notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id
    ).first()

    if not db_notification:
        raise HTTPException(
            status_code=404,
            detail="Notification tidak ditemukan"
        )

    db_notification.customer_id = notification.customer_id
    db_notification.title = notification.title
    db_notification.message = notification.message

    db.commit()
    db.refresh(db_notification)

    return db_notification


def delete_notification(
    db: Session,
    notification_id: int
):

    db_notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id
    ).first()

    if not db_notification:
        raise HTTPException(
            status_code=404,
            detail="Notification tidak ditemukan"
        )

    db.delete(db_notification)
    db.commit()

    return {
        "message": "Notification berhasil dihapus"
    }

# =====================================================
# DASHBOARD CRUD
# =====================================================

def get_dashboard_stats(db: Session):
    try:
        # 1. Hitung Status Order (Gunakan count langsung)
        active_orders = db.query(models.Order).filter(
            models.Order.status.in_(["pending", "processing"])
        ).count()

        done_orders = db.query(models.Order).filter(
            models.Order.status == "done"
        ).count()

        taken_orders = db.query(models.Order).filter(
            models.Order.status == "taken"
        ).count()

        total_orders = db.query(models.Order).count()

        # 2. Hitung Income & Expense (Gunakan func.sum agar aman jika data NULL)
        # .scalar() or 0 memastikan jika database kosong, hasilnya angka 0, bukan None
        total_income = db.query(func.sum(models.Payment.amount_paid)).filter(
            models.Payment.payment_status == "paid"
        ).scalar() or 0

        total_expense = db.query(func.sum(models.Expense.amount)).scalar() or 0

        # 3. Omzet Mingguan (Gunakan func.date untuk MySQL)
        weekly = []
        today = datetime.now().date()
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            # Perbaikan: Menggunakan func.date() karena MySQL lebih stabil dibanding .like()
            day_income = db.query(func.sum(models.Payment.amount_paid)).filter(
                models.Payment.payment_status == "paid",
                func.date(models.Payment.payment_date) == day
            ).scalar() or 0
            
            weekly.append({
                "label": day.strftime("%a"), # Contoh: Mon, Tue
                "amount": int(day_income)
            })

        # 4. Omzet Bulanan
        monthly = []
        for i in range(3, -1, -1):
            week_start = today - timedelta(weeks=i + 1)
            week_end   = today - timedelta(weeks=i)
            
            # Perbaikan: Bandingkan objek tanggal langsung, jangan diconvert ke string
            week_income = db.query(func.sum(models.Payment.amount_paid)).filter(
                models.Payment.payment_status == "paid",
                models.Payment.payment_date >= week_start,
                models.Payment.payment_date <= week_end
            ).scalar() or 0
            
            monthly.append({
                "label": f"W{4 - i}",
                "amount": int(week_income)
            })

        # 5. Return Data (Pastikan semua angka di-cast ke INT agar Android GSON tidak error)
        return {
            "active_orders": int(active_orders),
            "done_orders": int(done_orders),
            "taken_orders": int(taken_orders),
            "total_orders": int(total_orders),
            "total_income": int(total_income),
            "total_expense": int(total_expense),
            "total_profit": int(total_income - total_expense),
            "weekly_income": weekly,
            "monthly_income": monthly,
        }

    except Exception as e:
        # Jika ada error, akan muncul di terminal Python kamu
        print(f"Error pada get_dashboard_stats: {str(e)}")
        # Melempar error agar kita tahu masalahnya apa
        raise e