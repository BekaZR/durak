from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.join.command import JoinCommand
from domain.command.join.schema import JoinRequestSchema
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from db.crud.game import GameCRUD
from domain.command.seat.exception import SeatNotExist


class GameEndStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game_crud = GameCRUD()
        await game_crud.delete(room.id)
        return game


class GameStartExecuteClassicStrategy(GameStrategy):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.seats is None:
            raise SeatNotExist()
        for user_id, seat in request.seats.items():
            obj_in = JoinRequestSchema(
                user=seat.user.user, command="join", position=seat.position
            )
            request.request = obj_in
            await JoinCommand().execute(request=request, game=game, room=room)
        return game
