import json
from typing import Any, Optional


class UnAuthorizedException(BaseException):
    pass


class InvalidUUIDError(BaseException):
    pass


class APIError(Exception):
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[Any] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

    def __str__(self):
        details = (
            f"Status: {self.status_code}" if self.status_code else "Status: Unknown"
        )
        if self.response_body:
            try:
                jsonable_response_body = json.dumps(
                    json.loads(self.response_body), indent=4
                )
                details += f", Body: {jsonable_response_body}"
            except json.JSONDecodeError:
                details += f", Body: {self.response_body}"

        return f"{super().__str__()} ({details})"


class MismatchingExpectedStatusCodeError(APIError):
    pass


class DependencyError(Exception):
    pass
