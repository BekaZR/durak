from domain.command.turn.service import TurnService
from db.models.room import Room
from domain.command.base import Command
from domain.command.game.schema import GameSchema
from domain.command.user.exception import UserNotFound
from domain.state.schema import GameStateSchema


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
        await self.notify_room(request, game, room)
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

        await self.notify_room(request, game, room)
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
