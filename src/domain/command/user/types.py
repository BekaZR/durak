from typing import Annotated, NewType


UserId = NewType("UserId", int)

UserID = Annotated[int, "UserID"]
