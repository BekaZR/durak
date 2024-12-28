import asyncio
from domain.command.seat.schema import SeatSchema
from domain.command.turn.service import TurnService
from domain.command.user.schema import (
    BaseUserSchema,
    UserAchieved,
    UserConnect,
    UserSchema,
)
from domain.command.user.types import UserID


async def test_turn_service() -> None:
    seats: dict[UserID, SeatSchema] = {}
    for user_id in range(4):
        seat = SeatSchema(
            user=UserSchema(
                user=BaseUserSchema(user_id=user_id, username=f"{user_id}"),
                achieved=UserAchieved.PROCESSING,
                connect=UserConnect.CONNECTED,
                cards=[],
            ),
            position=user_id,
        )
        seats[user_id] = seat

    turn_service = TurnService()

    turn_schema = turn_service.create_all_players_queue(attacker_id=0, seats=seats)

    print(turn_schema.model_dump())
    # turn_schema.queue.pop(0)
    # turn_schema.queue.pop(0)
    # # turn_schema.queue.pop(0)
    # turn_schema.queue.pop(0)
    # seats[3].user.achieved = UserAchieved.WIN

    # print(turn_schema.model_dump())
    turn_schema.queue.pop(0)
    turn_schema = await turn_service.restore_turn_system_all_players(
        current_turn=turn_schema, seats=seats
    )
    turn_schema.queue.pop(0)
    turn_schema = await turn_service.restore_turn_system_all_players(
        current_turn=turn_schema, seats=seats
    )
    turn_schema.queue.pop(0)
    turn_schema = await turn_service.restore_turn_system_all_players(
        current_turn=turn_schema, seats=seats
    )
    print(turn_schema.model_dump())


asyncio.run(test_turn_service())
