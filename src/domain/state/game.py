from domain.command.game.schema import GameSchema
from domain.state.base import GameState
from domain.state.schema import GameStateSchema
from db.models.room import Room
from domain.command.user.schema import UserAchieved
from domain.command.game.enums import GameStatus


class GameEndState(GameState):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        active_user_count: int = 0
        for _, seat in game.seats.items():
            if seat.user.achieved == UserAchieved.PROCESSING:
                active_user_count += 1
                request.user = seat.user.user
        match active_user_count:
            case 1:
                game.status = GameStatus.FINISHED
            case _:
                request.user = None
                pass
        return game
