import pytest
from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.use_cases.release_lock import ReleaseLockUseCase


@pytest.mark.asyncio
async def test_release_lock_success(test_db: AsyncSession):
    repository = UserRepository(test_db)
    use_case = ReleaseLockUseCase(repository)
    project_id = uuid4()
    
    user = await repository.create(
        login="test@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    await repository.update_locktime(user.id, datetime.utcnow())
    
    result = await use_case.execute(user.id)
    
    assert result.user_id == user.id
    
    updated_user = await repository.get_by_id(user.id)
    assert updated_user.locktime is None


@pytest.mark.asyncio
async def test_release_lock_user_not_found(test_db: AsyncSession):
    repository = UserRepository(test_db)
    use_case = ReleaseLockUseCase(repository)
    non_existent_id = uuid4()
    
    with pytest.raises(HTTPException) as exc_info:
        await use_case.execute(non_existent_id)
    
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_release_lock_not_locked(test_db: AsyncSession):
    repository = UserRepository(test_db)
    use_case = ReleaseLockUseCase(repository)
    project_id = uuid4()
    
    user = await repository.create(
        login="test@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    with pytest.raises(HTTPException) as exc_info:
        await use_case.execute(user.id)
    
    assert exc_info.value.status_code == 409

