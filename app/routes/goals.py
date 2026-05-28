from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.models import User, Goal
from app.schemas.schemas import GoalCreate
from app.auth.security import get_current_user

router = APIRouter(prefix="/goals", tags=["Financial Goals"])

@router.post("/")
def create_goal(
    data: GoalCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = Goal(
        title=data.title,
        target_amount=data.target_amount,
        user_id=current_user.id
    )

    db.add(goal)
    db.commit()
    db.refresh(goal)

    return goal


@router.get("/")
def list_goals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Goal).filter(
        Goal.user_id == current_user.id
    ).all()


@router.patch("/{goal_id}/progress")
def update_goal_progress(
    goal_id: int,
    current_amount: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    goal = db.query(Goal).filter(
        Goal.id == goal_id,
        Goal.user_id == current_user.id
    ).first()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")

    goal.current_amount = current_amount

    db.commit()
    db.refresh(goal)

    return goal