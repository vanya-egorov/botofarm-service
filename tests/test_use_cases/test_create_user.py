import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.use_cases.create_user import CreateUserUseCase
from app.schemas.user import UserCreate


@pytest.mark.asyncio
async def test_create_user_use_case(test_db: AsyncSession):
    repository = UserRepository(test_db)
    use_case = CreateUserUseCase(repository)
    project_id = uuid4()
    
    user_data = UserCreate(
        login="test@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    result = await use_case.execute(user_data)
    
    assert result.id is not None
    assert result.login == "test@example.com"
    assert result.project_id == project_id
    assert result.env == "prod"
    assert result.domain == "regular"

