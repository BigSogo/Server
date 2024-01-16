from typing import TypeVar, Optional, Generic
from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    code: int
    message: str
    data: Optional[T] = None