from pydantic import ValidationError


def validation_exception_handler(exc: ValidationError) -> str:
    return exc.json(indent=4)
