from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from models import User, Expense
from security import hash_password, verify_password


# ---------------- USER ----------------
def create_user(db: Session, user):
    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user


# ---------------- EXPENSE ----------------
def create_expense(db: Session, expense, user_id: int):
    db_exp = Expense(
        amount=expense.amount,
        category=expense.category,
        note=expense.note,
        user_id=user_id
    )
    db.add(db_exp)
    db.commit()
    db.refresh(db_exp)
    return db_exp


def get_expenses(db: Session, user_id: int):
    return db.query(Expense).filter(Expense.user_id == user_id).all()