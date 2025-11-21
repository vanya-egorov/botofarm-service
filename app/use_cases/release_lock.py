from uuid import UUID
from fastapi import HTTPException

from app.repositories.user_repository import UserRepository
from app.schemas.user import UnlockResponse
from app.infrastructure.logging_config import logger


class ReleaseLockUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: UUID) -> UnlockResponse:
        logger.info(f"attempting to release lock for user: {user_id}")
        user = await self.repository.get_by_id(user_id)
        
        if not user:
            logger.warning(f"user not found: {user_id}")
            raise HTTPException(status_code=404, detail="user not found")
        
        if user.locktime is None:
            logger.warning(f"user is not locked: {user_id}")
            raise HTTPException(status_code=409, detail="user is not locked")
        
        updated_user = await self.repository.update_locktime(user_id, None)
        
        if not updated_user:
            logger.error(f"failed to release lock for user: {user_id}")
            raise HTTPException(status_code=500, detail="failed to release lock")
        
        logger.info(f"lock released successfully for user: {user_id}")
        return UnlockResponse(
            message="lock released successfully",
            user_id=updated_user.id,
        )

