import pytest
from uuid import uuid4
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository

ADMIN_TOKEN = "admin-secret"
HEADERS = {"Authorization": f"Bearer {ADMIN_TOKEN}"}


@pytest.mark.asyncio
async def test_create_user_endpoint(client: AsyncClient, test_db: AsyncSession):
    repository = UserRepository(test_db)
    project_id = uuid4()
    
    response = await client.post(
        "/users/",
        json={
            "login": "newuser@example.com",
            "password": "password123",
            "project_id": str(project_id),
            "env": "prod",
            "domain": "regular",
        },
        headers=HEADERS,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["login"] == "newuser@example.com"
    assert "password" not in data


@pytest.mark.asyncio
async def test_get_users_endpoint(client: AsyncClient, test_db: AsyncSession):
    repository = UserRepository(test_db)
    project_id = uuid4()
    
    await repository.create(
        login="user1@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    response = await client.get("/users/", headers=HEADERS)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["users"]) >= 1


@pytest.mark.asyncio
async def test_acquire_lock_endpoint(client: AsyncClient, test_db: AsyncSession):
    repository = UserRepository(test_db)
    project_id = uuid4()
    
    target_user = await repository.create(
        login="target@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    response = await client.post(
        "/users/acquire-lock",
        json={"user_id": str(target_user.id)},
        headers=HEADERS,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == str(target_user.id)
    assert "locked_at" in data


@pytest.mark.asyncio
async def test_release_lock_endpoint(client: AsyncClient, test_db: AsyncSession):
    from datetime import datetime
    
    repository = UserRepository(test_db)
    project_id = uuid4()
    
    target_user = await repository.create(
        login="target@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    await repository.update_locktime(target_user.id, datetime.utcnow())
    
    response = await client.post(
        "/users/release-lock",
        json={"user_id": str(target_user.id)},
        headers=HEADERS,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == str(target_user.id)


@pytest.mark.asyncio
async def test_acquire_lock_already_locked(client: AsyncClient, test_db: AsyncSession):
    from datetime import datetime
    
    repository = UserRepository(test_db)
    project_id = uuid4()
    
    target_user = await repository.create(
        login="target@example.com",
        password="password123",
        project_id=project_id,
        env="prod",
        domain="regular",
    )
    
    await repository.update_locktime(target_user.id, datetime.utcnow())
    
    response = await client.post(
        "/users/acquire-lock",
        json={"user_id": str(target_user.id)},
        headers=HEADERS,
    )
    
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/users/")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_invalid_token(client: AsyncClient):
    headers = {"Authorization": "Bearer invalid-token"}
    response = await client.get("/users/", headers=headers)
    assert response.status_code == 401
