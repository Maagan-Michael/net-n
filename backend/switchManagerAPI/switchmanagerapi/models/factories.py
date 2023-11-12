from enum import Enum
from pydantic import BaseModel, ConfigDict, UUID4


class OrderBy(str, Enum):
    """to order results in a paginated request"""
    asc = "asc"
    desc = "desc"


class BatchError(BaseModel):
    """Batch error model"""
    id: str | int | UUID4 = ""
    error: str = ""


def batcheableOutputFactory(model):
    """return a batcheable output model"""
    model_config = ConfigDict(from_attributes=True)

    class BatcheableOutputModel(BaseModel):
        """batcheable output model"""
        items: list[model] = []
        errors: list[BatchError] = []
    return BatcheableOutputModel


BatchedDeleteOutput = batcheableOutputFactory(str)
