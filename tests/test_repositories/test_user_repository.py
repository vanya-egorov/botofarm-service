import pytest
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.entities.user import User


@pytest.mark.asyncio
async def test_create_user(test_db: AsyncSession):
    repository = UserRepository(test_db)
    project_id = uuid4()
    
    user = await repository.create(
        login="test@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    assert user.id is not None
    assert user.login == "test@example.com"
    assert user.password != "password123"
    assert user.project_id == project_id
    assert user.env == "prod"
    assert user.domain == "regular"
    assert user.locktime is None


@pytest.mark.asyncio
async def test_get_by_id(test_db: AsyncSession):
    repository = UserRepository(test_db)
    project_id = uuid4()
    
    created_user = await repository.create(
        login="test@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    found_user = await repository.get_by_id(created_user.id)
    
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.login == "test@example.com"


@pytest.mark.asyncio
async def test_get_by_id_not_found(test_db: AsyncSession):
    repository = UserRepository(test_db)
    non_existent_id = uuid4()
    
    found_user = await repository.get_by_id(non_existent_id)
    
    assert found_user is None


@pytest.mark.asyncio
async def test_get_by_login(test_db: AsyncSession):
    repository = UserRepository(test_db)
    project_id = uuid4()
    
    created_user = await repository.create(
        login="test@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    found_user = await repository.get_by_login("test@example.com")
    
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.login == "test@example.com"


@pytest.mark.asyncio
async def test_get_all(test_db: AsyncSession):
    repository = UserRepository(test_db)
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
    
    users = await repository.get_all()
    
    assert len(users) == 2


@pytest.mark.asyncio
async def test_update_locktime(test_db: AsyncSession):
    from datetime import datetime
    
    repository = UserRepository(test_db)
    project_id = uuid4()
    
    user = await repository.create(
        login="test@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    assert user.locktime is None
    
    locktime = datetime.utcnow()
    updated_user = await repository.update_locktime(user.id, locktime)
    
    assert updated_user is not None
    assert updated_user.locktime is not None
    
    unlocked_user = await repository.update_locktime(user.id, None)
    
    assert unlocked_user is not None
    assert unlocked_user.locktime is None

