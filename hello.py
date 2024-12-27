from pprint import pprint
from domain.command.seat.schema import SeatSchema
from domain.command.turn.service import TurnService
from domain.command.user.schema import UserSchema, BaseUserSchema, UserAchieved
from domain.command.user.types import UserID


def test_create__players_queue() -> None:
    """Test creating queue where all players can participate"""
    seats: dict[UserID, SeatSchema] = {}
    for i in range(6):
        seats[i] = SeatSchema(
            user=UserSchema(
                user=BaseUserSchema(user_id=i, username=f"Player{i}"),
                cards=[],
                achieved=UserAchieved.PROCESSING,
            ),
            position=i,
        )
    # pprint(seats)
    seats[3].user.achieved = UserAchieved.WIN
    seats[4].user.achieved = UserAchieved.WIN
    seats[5].user.achieved = UserAchieved.WIN
    seats[0].user.achieved = UserAchieved.WIN
    queue = TurnService().create_neighbors_queue(attacker_id=1, seats=seats)
    print()
    pprint(queue.model_dump())

    # print(
    #     TurnService().get_next_round_attacker_defender_took_card(
    #         current_turn=queue, seats=seats
    #     )
    # )


test_create__players_queue()
