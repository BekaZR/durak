from domain.user.types import UserID
from schemas.base import BaseSchema


class TurnSchema(BaseSchema):
    currenct_attacker_user_id: UserID
    current_defender_user_id: UserID
    queue: list[UserID]
