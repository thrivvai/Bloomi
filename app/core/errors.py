from fastapi import Request, status
from fastapi.responses import JSONResponse


class BloomiError(Exception):
    def __init__(self, message: str, code: str, status_code: int = 400) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(BloomiError):
    def __init__(self, resource: str, resource_id: str | None = None) -> None:
        detail = f"{resource} not found"
        if resource_id:
            detail = f"{resource} '{resource_id}' not found"
        super().__init__(detail, "not_found", status.HTTP_404_NOT_FOUND)


class ConflictError(BloomiError):
    def __init__(self, message: str) -> None:
        super().__init__(message, "conflict", status.HTTP_409_CONFLICT)


class ForbiddenError(BloomiError):
    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(message, "forbidden", status.HTTP_403_FORBIDDEN)


class ValidationError(BloomiError):
    def __init__(self, message: str) -> None:
        super().__init__(message, "validation_error", status.HTTP_422_UNPROCESSABLE_ENTITY)


async def bloomi_error_handler(request: Request, exc: BloomiError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": {"code": "internal_error", "message": "An unexpected error occurred"}},
    )
