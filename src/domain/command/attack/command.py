from typing import Optional
from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.attack.schema import AttackRequestSchema, AttackResponseSchema
from domain.command.base import Command
from domain.command.game.schema import GameSchema
from domain.command.round.exception import RoundNotExistError
from domain.command.slot.schema import SlotOutSchema
from domain.state.schema import GameStateSchema
from exception.support import RequestNotSupportedError


class AttackCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        if not game.round:
            raise RoundNotExistError()
        game.round.slots.append(
            SlotOutSchema(attacker=obj_in.user, attacker_card=obj_in.card, status=False)
        )
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        raise NotImplementedError

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        if not game.round:
            raise RoundNotExistError()
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=AttackResponseSchema(
                command="attack",
                user=obj_in.user,
                position=game.seats[obj_in.user.user_id].position,
                card=obj_in.card,
            ).model_dump(mode="json"),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError
