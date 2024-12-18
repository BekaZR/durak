from datetime import UTC, datetime
from db.crud.game import GameCRUD
from db.crud.room import RoomCRUD
from db.enums.room import CardTransferPermission, DeckSize, PlayerCount, WalletType
from domain.game.command import CreateGameCommand, GameReadyCommand
from core.lifespan import session_factory
from domain.join.command import JoinCommand
from domain.join.schema import JoinRequestSchema
from domain.room.schema import RoomCreateSchema
from domain.timer.command import CreateTimerCommand
from domain.user.schema import BaseUserSchema


async def main() -> None:
    async with session_factory() as session:
        room_crud = RoomCRUD(session=session)
        room = await room_crud.create(
            RoomCreateSchema(
                bet_amount=10,
                player_count=PlayerCount.TWO,
                deck_size=DeckSize.SMALL,
                is_test=True,
                is_private=True,
                password="test",
                balance_type=WalletType.BONUS_BALANCE,
                created_at=datetime.now(tz=UTC),
                is_speed_mode=True,
                is_transfer_allowed=True,
                is_cheating_allowed=True,
                is_draw_allowed=True,
                card_transfer_permission=CardTransferPermission.NEIGHBORS_ONLY,
            )
        )
    game_crud = GameCRUD()
    game = await CreateGameCommand().execute(request=None, game=None, room=room)
    player1 = BaseUserSchema(user_id=1, username="player1")
    player2 = BaseUserSchema(user_id=2, username="player2")
    join_request = JoinRequestSchema(command="join", user=player1, position=0)
    join_request2 = JoinRequestSchema(command="join", user=player2, position=1)
    await JoinCommand().execute(request=join_request, game=game, room=room)
    await JoinCommand().execute(request=join_request2, game=game, room=room)
    await GameReadyCommand().execute(request=None, game=game, room=room)

    await CreateTimerCommand().execute(user=player1, game=game, room=room)
    await CreateTimerCommand().execute(user=player2, game=game, room=room)

    await game_crud.update(game, room.id)
    TakeCommand


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
