from datetime import datetime
from uuid import UUID
from fastapi import HTTPException

from app.repositories.user_repository import UserRepository
from app.schemas.user import LockResponse
from app.infrastructure.logging_config import logger


class AcquireLockUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: UUID) -> LockResponse:
        logger.info(f"attempting to acquire lock for user: {user_id}")
        user = await self.repository.get_by_id(user_id)
        
        if not user:
            logger.warning(f"user not found: {user_id}")
            raise HTTPException(status_code=404, detail="user not found")
        
        if user.locktime is not None:
            logger.warning(f"user already locked: {user_id}")
            raise HTTPException(status_code=409, detail="user is already locked")
        
        locktime = datetime.utcnow()
        updated_user = await self.repository.update_locktime(user_id, locktime)
        
        if not updated_user:
            logger.error(f"failed to update locktime for user: {user_id}")
            raise HTTPException(status_code=500, detail="failed to acquire lock")
        
        logger.info(f"lock acquired successfully for user: {user_id}")
        return LockResponse(
            message="lock acquired successfully",
            user_id=updated_user.id,
            locked_at=updated_user.locktime,
        )

