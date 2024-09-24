from pydantic import BaseModel
from pydantic import field_validator


class DefaultSchema(BaseModel):
    query_parameter: str

    @field_validator("query_parameter")  # noqa
    @classmethod
    def check_if_valid(cls, value: str):
        if value != "":
            return value
