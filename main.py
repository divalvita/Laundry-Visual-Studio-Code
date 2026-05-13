from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session


import models
import schemas
import crud

from database import SessionLocal, engine

# =========================================
# CREATE DATABASE
# =========================================

models.Base.metadata.create_all(bind=engine)

# =========================================
# FASTAPI APP
# =========================================

app = FastAPI(
    title="LaundryKu API",
    description="Smart Laundry Management System API",
    version="1.0.0"
)

# =========================================
# DATABASE DEPENDENCY
# =========================================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# =========================================
# ROOT
# =========================================

@app.get("/")
def root():
    return {
        "message": "LaundryKu API Running"
    }


# =========================================
# USERS ENDPOINT
# =========================================

@app.get("/users/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)


@app.get("/users/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):

    user = crud.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    return user

@app.put("/users/{user_id}",
         response_model=schemas.UserOut)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db)
):

    return crud.update_user(
        db,
        user_id,
        user
    )

@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    return crud.delete_user(
        db,
        user_id
    )


@app.post("/users/", response_model=schemas.UserOut)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):

    # sementara password belum di-hash
    hashed_password = user.password

    return crud.create_user(
        db,
        user,
        hashed_password
    )


# =========================================
# CUSTOMERS ENDPOINT
# =========================================

@app.get("/customers/", response_model=list[schemas.CustomerOut])
def get_customers(db: Session = Depends(get_db)):
    return crud.get_customers(db)


@app.post("/customers/", response_model=schemas.CustomerOut)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):
    return crud.create_customer(db, customer)


@app.put("/customers/{customer_id}",
         response_model=schemas.CustomerOut)
def update_customer(
    customer_id: int,
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):
    return crud.update_customer(
        db,
        customer_id,
        customer
    )


@app.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_customer(db, customer_id)


# =========================================
# CATEGORY ENDPOINT
# =========================================

@app.get("/categories/",
         response_model=list[schemas.CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)


@app.post("/categories/",
          response_model=schemas.CategoryOut)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    return crud.create_category(db, category)

@app.put("/categories/{category_id}",
         response_model=schemas.CategoryOut)
def update_category(
    category_id: int,
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):

    return crud.update_category(
        db,
        category_id,
        category
    )

@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):

    return crud.delete_category(
        db,
        category_id
    )


# =========================================
# SERVICES ENDPOINT
# =========================================

@app.get("/services/",
         response_model=list[schemas.ServiceOut])
def get_services(db: Session = Depends(get_db)):
    return crud.get_services(db)


@app.get("/services/{service_id}",
         response_model=schemas.ServiceOut)
def get_service(
    service_id: int,
    db: Session = Depends(get_db)
):

    service = crud.get_service_by_id(
        db,
        service_id
    )

    if not service:
        raise HTTPException(
            status_code=404,
            detail="Service tidak ditemukan"
        )

    return service


@app.post("/services/",
          response_model=schemas.ServiceOut)
def create_service(
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db)
):
    return crud.create_service(db, service)


@app.put("/services/{service_id}",
         response_model=schemas.ServiceOut)
def update_service(
    service_id: int,
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db)
):
    return crud.update_service(
        db,
        service_id,
        service
    )


@app.delete("/services/{service_id}")
def delete_service(
    service_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_service(db, service_id)


# =========================================
# ORDERS ENDPOINT
# =========================================

@app.get("/orders/",
         response_model=list[schemas.OrderOut])
def get_orders(db: Session = Depends(get_db)):
    return crud.get_orders(db)


@app.get("/orders/{order_id}",
         response_model=schemas.OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = crud.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order tidak ditemukan"
        )

    return order


@app.post("/orders/",
          response_model=schemas.OrderOut)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):

    # sementara hardcode user admin
    current_user_id = 1

    return crud.create_order(
        db,
        order,
        current_user_id
    )


@app.put("/orders/{order_id}",
         response_model=schemas.OrderOut)
def update_order_status(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_order_status(
        db,
        order_id,
        order_update
    )


@app.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_order(db, order_id)


# =========================================
# PAYMENTS ENDPOINT
# =========================================

@app.get("/payments/",
         response_model=list[schemas.PaymentOut])
def get_payments(db: Session = Depends(get_db)):
    return crud.get_payments(db)


@app.post("/payments/",
          response_model=schemas.PaymentOut)
def create_payment(
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_payment(db, payment)

@app.put("/payments/{payment_id}",
         response_model=schemas.PaymentOut)
def update_payment(
    payment_id: int,
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db)
):

    return crud.update_payment(
        db,
        payment_id,
        payment
    )


@app.delete("/payments/{payment_id}")
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):

    return crud.delete_payment(
        db,
        payment_id
    )


# =========================================
# EXPENSES ENDPOINT
# =========================================

@app.get("/expenses/",
         response_model=list[schemas.ExpenseOut])
def get_expenses(db: Session = Depends(get_db)):
    return crud.get_expenses(db)


@app.post("/expenses/",
          response_model=schemas.ExpenseOut)
def create_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):
    return crud.create_expense(db, expense)

@app.put("/expenses/{expense_id}",
         response_model=schemas.ExpenseOut)
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):

    return crud.update_expense(
        db,
        expense_id,
        expense
    )


@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    return crud.delete_expense(
        db,
        expense_id
    )


# =========================================
# NOTIFICATIONS ENDPOINT
# =========================================

@app.get("/notifications/",
         response_model=list[schemas.NotificationOut])
def get_notifications(db: Session = Depends(get_db)):
    return crud.get_notifications(db)


@app.post("/notifications/",
          response_model=schemas.NotificationOut)
def create_notification(
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db)
):
    return crud.create_notification(
        db,
        notification
    )

@app.put("/notifications/{notification_id}",
         response_model=schemas.NotificationOut)
def update_notification(
    notification_id: int,
    notification: schemas.NotificationCreate,
    db: Session = Depends(get_db)
):

    return crud.update_notification(
        db,
        notification_id,
        notification
    )


@app.delete("/notifications/{notification_id}")
def delete_notification(
    notification_id: int,
    db: Session = Depends(get_db)
):

    return crud.delete_notification(
        db,
        notification_id
    )