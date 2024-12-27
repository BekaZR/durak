from domain.command.round.enum import RoundEnum
from domain.command.round.exception import RoundNotExistError
from domain.command.turn.service import TurnService
from db.models.room import Room
from domain.command.base import Command
from domain.command.game.schema import GameSchema
from domain.command.user.exception import UserNotFound
from domain.state.schema import GameStateSchema
from domain.command.turn.exception import TurnNotExistError


class CreateAllPlayersTurnCommand(Command):
    """Команда создания очереди, где подкидывать могут все игроки"""

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.user is None:
            raise UserNotFound()
        turn_service = TurnService()
        game.turn = turn_service.create_all_players_queue(
            seats=game.seats, attacker_id=request.user.user_id
        )
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.turn = None
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class CreateNeighborsTurnCommand(Command):
    """Команда создания очереди, где подкидывать могут только соседи"""

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if request.user is None:
            raise UserNotFound()
        turn_service = TurnService()
        game.turn = turn_service.create_neighbors_queue(
            seats=game.seats, attacker_id=request.user.user_id
        )

        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.turn = None
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class TurnSetNextAttackerCommand(Command):
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
        match game.round.status:
            case RoundEnum.TAKE:
                next_attacker_id = turn_service.find_next_attacker_after_take(
                    current_turn=game.turn,
                    seats=game.seats,
                )
        request.user = game.seats[next_attacker_id].user.user
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        game.turn = None
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
