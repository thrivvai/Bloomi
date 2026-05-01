from pydantic import BaseModel


class OkResponse(BaseModel):
    ok: bool = True


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
