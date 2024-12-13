from typing import TypeVar
from domain.schema import BaseRequestSchema


TBaseRequestSchema = TypeVar("TBaseRequestSchema", bound=BaseRequestSchema)
