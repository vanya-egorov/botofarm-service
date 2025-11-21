import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.use_cases.get_users import GetUsersUseCase


@pytest.mark.asyncio
async def test_get_users_use_case(test_db: AsyncSession):
    repository = UserRepository(test_db)
    use_case = GetUsersUseCase(repository)
    project_id = uuid4()
    
    await repository.create(
        login="test1@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    await repository.create(
        login="test2@example.com",
        password="password123",
        project_id=project_id,
        env="stage",
        domain="canary",
    )
    
    result = await use_case.execute()
    
    assert len(result.users) == 2

