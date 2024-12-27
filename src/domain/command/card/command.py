from typing import Any, Optional
from core.manager import UserNotificationManager
from db.models.room import Room
from domain.command.attack.schema import AttackRequestSchema
from domain.command.card.exception import DeckEmptyError, TrumpNotExist
from domain.command.card.schema import CardOutSchema, CardSchema, DeckOutSchema
from domain.command.card.service import CardService
from domain.command.base import Command

from domain.command.game.schema import GameSchema
from domain.command.round.exception import RoundNotExistError
from domain.command.turn.exception import TrumpNotExistsException
from domain.command.user.exception import AttackerNotFound, UserNotFound
from domain.command.user.schema import BaseUserSchema
from domain.state.schema import GameStateSchema
from exception.support import RequestNotSupportedError


class CreateDeckCardCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        cards = CardService().create_deck(room.player_count)
        game.deck = cards
        return game

    async def rollback(self, request: Any, game: GameSchema, room: Room) -> GameSchema:
        game.deck = []
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        if game.trump is None:
            raise TrumpNotExist()
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=DeckOutSchema(
                command="deck", cards=len(game.deck), trump=game.trump
            ).model_dump(mode="json"),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        raise NotImplementedError


class RemoveUserCardCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        game.seats[obj_in.user.user_id].user.cards.remove(obj_in.card)
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        if obj_in.card not in game.seats[obj_in.user.user_id].user.cards:
            game.seats[obj_in.user.user_id].user.cards.append(obj_in.card)
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=CardOutSchema(command="card", action="remove", cards=1).model_dump(
                mode="json"
            ),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        await UserNotificationManager.send_personal_message(
            room_id=room.id,
            user=obj_in.user,
            message=CardOutSchema(command="card", action="remove", cards=1).model_dump(
                mode="json"
            ),
        )


class AddUserCardFromDeckCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[list[CardSchema]] = request.cards
        user: Optional[BaseUserSchema] = request.user
        if user is None or not isinstance(user, BaseUserSchema):
            raise UserNotFound()
        if obj_in is None or not all(isinstance(card, CardSchema) for card in obj_in):
            raise RequestNotSupportedError()
        game.seats[user.user_id].user.cards.extend(obj_in)
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        if obj_in.card not in game.seats[obj_in.user.user_id].user.cards:
            game.seats[obj_in.user.user_id].user.cards.append(obj_in.card)
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=CardOutSchema(command="card", action="remove", cards=1).model_dump(
                mode="json"
            ),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        await UserNotificationManager.send_personal_message(
            room_id=room.id,
            user=obj_in.user,
            message=CardOutSchema(command="card", action="remove", cards=1).model_dump(
                mode="json"
            ),
        )


class AddUserCardTableCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[list[CardSchema]] = request.cards
        user: Optional[BaseUserSchema] = request.user
        if user is None or not isinstance(user, BaseUserSchema):
            raise UserNotFound()
        if obj_in is None or not all(isinstance(card, CardSchema) for card in obj_in):
            raise RequestNotSupportedError()
        game.seats[user.user_id].user.cards.extend(obj_in)
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        if obj_in.card not in game.seats[obj_in.user.user_id].user.cards:
            game.seats[obj_in.user.user_id].user.cards.append(obj_in.card)
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=CardOutSchema(command="card", action="remove", cards=1).model_dump(
                mode="json"
            ),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        obj_in: Optional[AttackRequestSchema] = request.request
        if obj_in is None or not isinstance(obj_in, AttackRequestSchema):
            raise RequestNotSupportedError()
        await UserNotificationManager.send_personal_message(
            room_id=room.id,
            user=obj_in.user,
            message=CardOutSchema(command="card", action="remove", cards=1).model_dump(
                mode="json"
            ),
        )


class SetTrumpCardCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        """Установить козырную карту из последней карты в колоде."""
        if not game.deck:
            raise DeckEmptyError()

        # Устанавливаем последнюю карту колоды как козырь
        game.trump = game.deck[-1]
        # Уведомляем всех игроков о козыре
        await self.notify_room(request, game, room)
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        """Отменить установку козыря."""
        game.trump = None
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        """Уведомить всех игроков о козырной карте."""
        if game.trump is None:
            raise TrumpNotExist()

        await UserNotificationManager.send_room_message(
            room_id=room.id,
            message=DeckOutSchema(
                command="deck", trump=game.trump, cards=len(game.deck)
            ).model_dump(mode="json"),
        )

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        """Уведомить конкретного игрока о козырной карте."""
        raise NotImplementedError


class FindLowestCardPlayerCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        """Определить игрока с наименьшей картой."""
        if not game.trump:
            raise TrumpNotExistsException()
        card_service = CardService()
        user_id = await card_service.find_lowest_card_player(game)
        if not user_id:
            raise AttackerNotFound()
        request.user = game.seats[user_id].user.user
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        """Откат не требуется, так как команда не меняет состояние."""
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        """Уведомить всех игроков о игроке с наименьшей картой."""
        raise NotImplementedError

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        """Личные уведомления не требуются."""
        raise NotImplementedError


class AddCardToBeatCommand(Command):
    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        if game.round is None:
            raise RoundNotExistError()
        cards: list[CardSchema] = []
        for slot in game.round.slots:
            cards.append(slot.attacker_card)
            if not slot.enemy_card:
                continue
            cards.append(slot.enemy_card)
        game.deck.extend(cards)
        return game

    async def rollback(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        """Откат не требуется, так как команда не меняет состояние."""
        return game

    async def notify_room(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        """Уведомить всех игроков о игроке с наименьшей картой."""
        raise NotImplementedError

    async def notify_personal(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> None:
        """Личные уведомления не требуются."""
        raise NotImplementedError
