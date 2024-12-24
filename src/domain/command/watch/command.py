from typing import Optional
from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.attack.schema import AttackRequestSchema, AttackResponseSchema
from domain.command.base import Command
from domain.game.schema import GameOutSchema, GameSchema
from domain.command.round.exception import RoundNotExistError
from domain.seat.schema import SeatOutSchema
from domain.command.slot.schema import SlotOutSchema
from domain.state.schema import GameStateSchema
from domain.user.schema import UserOutSchema
from domain.watch.schema import WatchRequestSchema
from exception.support import RequestNotSupportedError


class WatchCommand(Command):
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
        obj_in: Optional[WatchRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, WatchRequestSchema):
            raise RequestNotSupportedError()
        game_out_schema = GameOutSchema(
            seats={},
            round=game.round,
            deck=game.deck,
            turn=game.turn,
            status=game.status,
        )
        for user_id, seat in game.seats.items():
            game_out_schema.seats[user_id] = SeatOutSchema(
                user=UserOutSchema(
                    user=seat.user.user,
                    cards=len(seat.user.cards),
                    connect=seat.user.connect,
                    achieved=seat.user.achieved,
                    is_ready=seat.user.is_ready,
                ),
                position=seat.position,
            )
        await UserNotificationManager.send_personal_message(
            room_id=room.id,
            user=obj_in.user,
            message=game_out_schema.model_dump(mode="json"),
        )
