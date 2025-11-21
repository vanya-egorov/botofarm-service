from fastapi import status
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db
from app.handlers.auth import verify_admin_token
from app.repositories.user_repository import UserRepository
from app.use_cases.create_user import CreateUserUseCase
from app.use_cases.get_users import GetUsersUseCase
from app.use_cases.acquire_lock import AcquireLockUseCase
from app.use_cases.release_lock import ReleaseLockUseCase
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserListResponse,
    LockRequest,
    LockResponse,
    UnlockResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Создание нового пользователя",
)
async def create_user(
    user_data: UserCreate,
    _: bool = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    repository = UserRepository(db)
    use_case = CreateUserUseCase(repository)
    return await use_case.execute(user_data)


@router.get(
    "/",
    response_model=UserListResponse,
    summary="Получение списка всех пользователей",
)
async def get_users(
    _: bool = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
) -> UserListResponse:
    repository = UserRepository(db)
    use_case = GetUsersUseCase(repository)
    return await use_case.execute()


@router.post(
    "/acquire-lock",
    response_model=LockResponse,
    summary="Блокировка пользователя",

)
async def acquire_lock(
    lock_request: LockRequest,
    _: bool = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
) -> LockResponse:
    repository = UserRepository(db)
    use_case = AcquireLockUseCase(repository)
    return await use_case.execute(lock_request.user_id)


@router.post(
    "/release-lock",
    response_model=UnlockResponse,
    summary="Разблокировка пользователя",
)
async def release_lock(
    lock_request: LockRequest,
    _: bool = Depends(verify_admin_token),
    db: AsyncSession = Depends(get_db),
) -> UnlockResponse:
    repository = UserRepository(db)
    use_case = ReleaseLockUseCase(repository)
    return await use_case.execute(lock_request.user_id)

