from fastapi import APIRouter, Body, Depends

from src.application.use_cases.users.delete_user import DeleteUser
from src.application.use_cases.users.get_roles import GetRoles
from src.application.use_cases.users.get_user_roles import GetUserRoles
from src.application.use_cases.users.get_users import GetUsers
from src.application.use_cases.users.set_roles import SetRoles
from src.config import ID, PREFIX_URL
from src.domain.entities import User
from src.domain.enums import RoleEnum
from src.infrastructure.managers.role_manager import roles
from src.presentation.dependencies.users_dependencies import UsersDependencies
from src.presentation.schemas import Role

router = APIRouter(
    prefix=PREFIX_URL + '/users',
    tags=['Users'],
)


@router.get(
    path='',
    summary='Получение пользователей',
    dependencies=[Depends(roles([RoleEnum.admin]))],
)
async def get_users(
    users: GetUsers = Depends(UsersDependencies.get_users),
) -> list[User]:
    return await users()


@router.patch(
    path='/{user_id}/roles',
    summary='Изменение роли у пользователя',
    dependencies=[Depends(roles([RoleEnum.admin]))],
)
async def set_user_roles(
    user_id: ID,
    roles: list[RoleEnum] = Body(examples=[[role.name for role in RoleEnum]]),
    set_role: SetRoles = Depends(UsersDependencies.set_roles),
):
    await set_role(user_id, roles)


@router.delete(
    path='/{user_id}',
    status_code=204,
    summary='Удаление пользователя',
    dependencies=[Depends(roles([RoleEnum.admin]))],
)
async def delete_user(
    user_id: ID, delete: DeleteUser = Depends(UsersDependencies.delete_user)
):
    await delete(user_id)


@router.get(
    path='/roles',
    summary='Получение ролей',
    dependencies=[Depends(roles([RoleEnum.admin]))],
)
async def get_roles(
    get_roles: GetRoles = Depends(UsersDependencies.get_roles),
) -> list[Role]:
    return await get_roles()


@router.get(
    path='/{user_id}/roles',
    summary='Получение ролей пользователя',
    dependencies=[Depends(roles([RoleEnum.admin]))],
)
async def get_user_roles(
    user_id: ID, get_roles: GetUserRoles = Depends(UsersDependencies.get_user_roles)
) -> list[Role]:
    return await get_roles(user_id)
