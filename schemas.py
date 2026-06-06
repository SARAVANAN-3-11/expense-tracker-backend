from pydantic import BaseModel


# ---------------- USER ----------------
class UserCreate(BaseModel):
    username: str
    password: str


# ---------------- CREATE EXPENSE ----------------
class ExpenseCreate(BaseModel):
    amount: float
    category: str
    note: str


# ---------------- UPDATE EXPENSE ----------------
class ExpenseUpdate(BaseModel):
    amount: float
    category: str
    note: str