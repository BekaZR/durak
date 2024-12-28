from pydantic.fields import Field
from domain.command.user.types import UserID
from schemas.base import BaseSchema


class TurnSchema(BaseSchema):
    currenct_attacker_user_id: UserID
    current_defender_user_id: UserID
    neigbor_user_id: UserID | None = Field(default=None)
    queue: list[UserID]
