from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse
from app.infrastructure.logging_config import logger


class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_data: UserCreate) -> UserResponse:
        logger.info(f"creating user with login: {user_data.login}")

        existing_user = await self.repository.get_by_login(user_data.login)
        logger.info(f"existing user check: {existing_user}")

        if existing_user:
            logger.warning(f"user with login {user_data.login} already exists")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user with login {user_data.login} already exists"
            )

        try:
            user = await self.repository.create(
                login=user_data.login,
                password=user_data.password,
                project_id=user_data.project_id,
                env=user_data.env,
                domain=user_data.domain,
            )
            logger.info(f"user created successfully with id: {user.id}")
            return UserResponse.model_validate(user)
        except ValueError as e:
            logger.error(f"error creating user: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(e)
            ) from e
        except Exception as e:
            logger.error(f"unexpected error creating user: {type(e).__name__}: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"failed to create user: {str(e)}"
            ) from e

