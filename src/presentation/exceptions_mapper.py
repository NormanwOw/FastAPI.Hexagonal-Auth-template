from fastapi import HTTPException

from src.domain import exceptions as d_exc

exceptions_mapper = {
    d_exc.RoleMismatch: HTTPException(status_code=403, detail='Role mismatch'),
    d_exc.RoleNotFoundException: HTTPException(
        status_code=404, detail='Role not found'
    ),
    d_exc.NoTokenProvidedException: HTTPException(
        status_code=403, detail='No token provided'
    ),
    d_exc.RoleRequiredException: HTTPException(status_code=403, detail='Role required'),
    d_exc.InvalidUsernameException: HTTPException(
        status_code=403, detail='Invalid username'
    ),
    d_exc.UsernameAlreadyExistsException: HTTPException(
        status_code=403, detail='Username already exists'
    ),
    d_exc.NotAuthenticatedException: HTTPException(
        status_code=403, detail='Not authenticated'
    ),
    d_exc.TokenTypeMismatchException: HTTPException(
        status_code=403, detail='Token type mismatch'
    ),
    d_exc.UserNotFoundException: HTTPException(
        status_code=404, detail='User not found'
    ),
    d_exc.TokenInvalidatedException: HTTPException(
        status_code=403, detail='Token invalidated'
    ),
    d_exc.UserDisabledException: HTTPException(status_code=403, detail='User disabled'),
    d_exc.UnauthorizedException: HTTPException(status_code=403, detail='Unauthorized'),
    d_exc.InvalidPasswordException: HTTPException(
        status_code=403, detail='Invalid password'
    ),
    d_exc.PasswordConfirmationMissmatchException: HTTPException(
        status_code=422, detail='Confirm password mismatch'
    ),
    d_exc.InvalidTokenException: HTTPException(status_code=403, detail='Invalid token'),
}
