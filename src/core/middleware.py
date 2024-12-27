import uuid
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from core.logger import RequestContext, request_context_var


class LogRequestIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("x-request-id")

        if not request_id:
            request_id = str(uuid.uuid4())

        request_context = RequestContext(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else "",
        )
        request_context_var.set(request_context)

        response: Response = await call_next(request)

        request_context.status_code = response.status_code
        request_context_var.set(request_context)
        response.headers["x-request-id"] = request_id

        return response
