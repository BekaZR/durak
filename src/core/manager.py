from domain.user.schema import BaseUserSchema


class UserNotificationManager:
    @classmethod
    async def send_personal_message(
        cls, room_id: int, user: BaseUserSchema, message: dict[str, str]
    ) -> None:
        ...

    @classmethod
    async def send_room_message(cls, room_id: int, message: dict[str, str]) -> None:
        ...
