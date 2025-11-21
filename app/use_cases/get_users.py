
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserListResponse, UserResponse
from app.infrastructure.logging_config import logger


class GetUsersUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self) -> UserListResponse:
        logger.info("fetching all users")
        users = await self.repository.get_all()
        logger.info(f"found {len(users)} users")
        return UserListResponse(users=[UserResponse.model_validate(user) for user in users])

