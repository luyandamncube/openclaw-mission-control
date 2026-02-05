from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, col, select

from app.api.deps import ActorContext, get_board_or_404, require_admin_or_agent
from app.db.session import get_session
from app.models.board_memory import BoardMemory
from app.schemas.board_memory import BoardMemoryCreate, BoardMemoryRead

router = APIRouter(prefix="/boards/{board_id}/memory", tags=["board-memory"])


@router.get("", response_model=list[BoardMemoryRead])
def list_board_memory(
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    board=Depends(get_board_or_404),
    session: Session = Depends(get_session),
    actor: ActorContext = Depends(require_admin_or_agent),
) -> list[BoardMemory]:
    if actor.actor_type == "agent" and actor.agent:
        if actor.agent.board_id and actor.agent.board_id != board.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    statement = (
        select(BoardMemory)
        .where(col(BoardMemory.board_id) == board.id)
        .order_by(col(BoardMemory.created_at).desc())
        .offset(offset)
        .limit(limit)
    )
    return list(session.exec(statement))


@router.post("", response_model=BoardMemoryRead)
def create_board_memory(
    payload: BoardMemoryCreate,
    board=Depends(get_board_or_404),
    session: Session = Depends(get_session),
    actor: ActorContext = Depends(require_admin_or_agent),
) -> BoardMemory:
    if actor.actor_type == "agent" and actor.agent:
        if actor.agent.board_id and actor.agent.board_id != board.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    memory = BoardMemory(
        board_id=board.id,
        content=payload.content,
        tags=payload.tags,
        source=payload.source,
    )
    session.add(memory)
    session.commit()
    session.refresh(memory)
    return memory
