from fastapi import Request, status
from fastapi.responses import JSONResponse


class CareerLensError(Exception):
    def __init__(self, message: str, code: str = "application_error") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


async def careerlens_exception_handler(request: Request, exc: CareerLensError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "request_id": getattr(request.state, "request_id", None),
            }
        },
    )
