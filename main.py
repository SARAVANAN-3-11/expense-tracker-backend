from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from db import Base, engine
import models, schemas
from dependencies import get_db

# ---------------- APP ----------------
app = FastAPI()

# ---------------- DB ----------------
Base.metadata.create_all(bind=engine)

# ---------------- PASSWORD ----------------
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str):
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password[:72], hashed_password)


# ---------------- REGISTER ----------------
@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    existing = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = models.User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }


# ---------------- LOGIN ----------------
@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "message": "Login success",
        "username": db_user.username
    }


# ---------------- ADD EXPENSE ----------------
@app.post("/expenses")
def add_expense(
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):

    new_expense = models.Expense(
        amount=expense.amount,
        category=expense.category,
        note=expense.note,
        user_id=1
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return {
        "message": "Expense added successfully"
    }


# ---------------- GET EXPENSES ----------------
@app.get("/expenses")
def get_expenses(
    db: Session = Depends(get_db)
):

    expenses = db.query(
        models.Expense
    ).all()

    return expenses


# ---------------- UPDATE EXPENSE ----------------
@app.put("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    expense: schemas.ExpenseCreate,
    db: Session = Depends(get_db)
):

    db_expense = db.query(
        models.Expense
    ).filter(
        models.Expense.id == expense_id
    ).first()

    if not db_expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db_expense.amount = expense.amount
    db_expense.category = expense.category
    db_expense.note = expense.note

    db.commit()
    db.refresh(db_expense)

    return {
        "message": "Expense updated successfully"
    }


# ---------------- DELETE EXPENSE ----------------
@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db)
):

    expense = db.query(
        models.Expense
    ).filter(
        models.Expense.id == expense_id
    ).first()

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    db.delete(expense)
    db.commit()

    return {
        "message": "Expense deleted successfully"
    }