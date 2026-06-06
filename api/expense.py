from datetime import date
from typing import Optional, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.app.db.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from backend.app.services.expense_service import (
    create_expense,
    get_expenses,
    get_expense_by_id,
    update_expense,
    delete_expense,
)

router = APIRouter(prefix="/api/expenses", tags=["Expenses"])


@router.post("/", response_model=ExpenseResponse, status_code=201)
def add_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a new expense (amount, category, date, note)."""
    expense = create_expense(db, expense_data, current_user.id)
    return ExpenseResponse(
        id=expense.id,
        amount=expense.amount,
        category_id=expense.category_id,
        category_name=expense.category.name if expense.category else None,
        date=expense.date,
        note=expense.note,
        user_id=expense.user_id,
        created_at=expense.created_at,
    )


@router.get("/", response_model=List[ExpenseResponse])
def list_expenses(
    start_date: Optional[date] = Query(None, description="Filter from this date"),
    end_date: Optional[date] = Query(None, description="Filter until this date"),
    category_id: Optional[int] = Query(None, description="Filter by category ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List expenses with optional date range and category filters."""
    expenses = get_expenses(db, current_user.id, start_date, end_date, category_id, skip, limit)
    return [
        ExpenseResponse(
            id=e.id,
            amount=e.amount,
            category_id=e.category_id,
            category_name=e.category.name if e.category else None,
            date=e.date,
            note=e.note,
            user_id=e.user_id,
            created_at=e.created_at,
        )
        for e in expenses
    ]


@router.put("/{expense_id}", response_model=ExpenseResponse)
def edit_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Edit an existing expense."""
    expense = update_expense(db, expense_id, current_user.id, expense_data)
    return ExpenseResponse(
        id=expense.id,
        amount=expense.amount,
        category_id=expense.category_id,
        category_name=expense.category.name if expense.category else None,
        date=expense.date,
        note=expense.note,
        user_id=expense.user_id,
        created_at=expense.created_at,
    )


@router.delete("/{expense_id}")
def remove_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete an expense by ID."""
    return delete_expense(db, expense_id, current_user.id)