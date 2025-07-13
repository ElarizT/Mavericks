from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import as_declarative
from sqlalchemy.dialects.postgresql import JSON
from typing import Any


@as_declarative()
class Base:
    type_annotations_map = {dict[str, Any]: JSON}

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"  # plural
