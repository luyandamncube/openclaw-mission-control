from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, col, select

from app.api.deps import ActorContext, get_board_or_404, require_admin_auth, require_admin_or_agent
from app.db.session import get_session
from app.models.approvals import Approval
from app.schemas.approvals import ApprovalCreate, ApprovalRead, ApprovalUpdate

router = APIRouter(prefix="/boards/{board_id}/approvals", tags=["approvals"])

ALLOWED_STATUSES = {"pending", "approved", "rejected"}


@router.get("", response_model=list[ApprovalRead])
def list_approvals(
    status_filter: str | None = Query(default=None, alias="status"),
    board=Depends(get_board_or_404),
    session: Session = Depends(get_session),
    actor: ActorContext = Depends(require_admin_or_agent),
) -> list[Approval]:
    if actor.actor_type == "agent" and actor.agent:
        if actor.agent.board_id and actor.agent.board_id != board.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    statement = select(Approval).where(col(Approval.board_id) == board.id)
    if status_filter:
        if status_filter not in ALLOWED_STATUSES:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        statement = statement.where(col(Approval.status) == status_filter)
    statement = statement.order_by(col(Approval.created_at).desc())
    return list(session.exec(statement))


@router.post("", response_model=ApprovalRead)
def create_approval(
    payload: ApprovalCreate,
    board=Depends(get_board_or_404),
    session: Session = Depends(get_session),
    actor: ActorContext = Depends(require_admin_or_agent),
) -> Approval:
    if actor.actor_type == "agent" and actor.agent:
        if actor.agent.board_id and actor.agent.board_id != board.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    approval = Approval(
        board_id=board.id,
        agent_id=payload.agent_id,
        action_type=payload.action_type,
        payload=payload.payload,
        confidence=payload.confidence,
        rubric_scores=payload.rubric_scores,
        status=payload.status,
    )
    session.add(approval)
    session.commit()
    session.refresh(approval)
    return approval


@router.patch("/{approval_id}", response_model=ApprovalRead)
def update_approval(
    approval_id: str,
    payload: ApprovalUpdate,
    board=Depends(get_board_or_404),
    session: Session = Depends(get_session),
    auth=Depends(require_admin_auth),
) -> Approval:
    approval = session.get(Approval, approval_id)
    if approval is None or approval.board_id != board.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    updates = payload.model_dump(exclude_unset=True)
    if "status" in updates:
        if updates["status"] not in ALLOWED_STATUSES:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
        approval.status = updates["status"]
        if approval.status != "pending":
            approval.resolved_at = datetime.utcnow()
    session.add(approval)
    session.commit()
    session.refresh(approval)
    return approval
