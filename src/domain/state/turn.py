from db.models.room import Room
from domain.command.game.schema import GameSchema
from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.turn.exception import TurnNotExistError
from domain.command.user.exception import UserNotFound
from domain.state.base import GameState
from domain.state.schema import GameStateSchema
from hello import TurnService


class SetNextAttackerState(GameState):
    """Команда создания очереди, где подкидывать могут только соседи"""

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.user is None:
            raise UserNotFound()
        if not game.turn:
            raise TurnNotExistError()
        if not game.round:
            raise RoundNotExistError()
        turn_service = TurnService()
        next_attacker_id = turn_service.find_next_attacker_after_defense(
            current_turn=game.turn,
            seats=game.seats,
        )
        match game.round.status:
            case RoundEnum.TAKE:
                next_attacker_id = turn_service.find_next_attacker_after_take(
                    current_turn=game.turn,
                    seats=game.seats,
                )
        request.user = game.seats[next_attacker_id].user.user
        return game
