import pytest
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.use_cases.acquire_lock import AcquireLockUseCase


@pytest.mark.asyncio
async def test_acquire_lock_success(test_db: AsyncSession):
    repository = UserRepository(test_db)
    use_case = AcquireLockUseCase(repository)
    project_id = uuid4()
    
    user = await repository.create(
        login="test@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    result = await use_case.execute(user.id)
    
    assert result.user_id == user.id
    assert result.locked_at is not None
    
    updated_user = await repository.get_by_id(user.id)
    assert updated_user.locktime is not None


@pytest.mark.asyncio
async def test_acquire_lock_user_not_found(test_db: AsyncSession):
    repository = UserRepository(test_db)
    use_case = AcquireLockUseCase(repository)
    non_existent_id = uuid4()
    
    with pytest.raises(HTTPException) as exc_info:
        await use_case.execute(non_existent_id)
    
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_acquire_lock_already_locked(test_db: AsyncSession):
    from datetime import datetime
    
    repository = UserRepository(test_db)
    use_case = AcquireLockUseCase(repository)
    project_id = uuid4()
    
    user = await repository.create(
        login="test@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    await repository.update_locktime(user.id, datetime.utcnow())
    
    with pytest.raises(HTTPException) as exc_info:
        await use_case.execute(user.id)
    
    assert exc_info.value.status_code == 409

