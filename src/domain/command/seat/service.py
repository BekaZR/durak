from domain.command.seat.schema import SeatSchema
from domain.command.user.types import UserID


class SeatService:
    async def get_user_count_with_cards(self, seats: dict[UserID, SeatSchema]) -> int:
        return len([seat for _, seat in seats.items() if len(seat.user.cards) != 0])
