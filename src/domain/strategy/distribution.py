from db.models.room import Room
from domain.command.card.command import AddUserCardFromDeckCommand, SetTrumpCardCommand
from domain.command.card.exception import DeckNotExistError
from domain.command.game.schema import GameSchema
from domain.state.schema import GameStateSchema
from domain.strategy.base import GameStrategy
from domain.command.user.schema import BaseUserSchema


class InitialDealStrategy(GameStrategy):
    INITIAL_CARDS_COUNT = 6

    async def execute(
        self, request: GameStateSchema, game: GameSchema, room: Room
    ) -> GameSchema:
        """Стратегия начальной раздачи карт"""
        if not game.deck:
            raise DeckNotExistError()

        # Устанавливаем козырь через отдельную команду
        await SetTrumpCardCommand().execute(request=request, game=game, room=room)

        # Раздаем каждому игроку пачку карт за раз
        for user_id, seat in game.seats.items():
            # Определяем сколько карт можем раздать
            cards_to_deal = min(self.INITIAL_CARDS_COUNT, len(game.deck))
            if not cards_to_deal:
                break

            # Берем пачку карт из колоды
            cards = game.deck[:cards_to_deal]
            game.deck = game.deck[cards_to_deal:]

            # Создаем состояние для команды
            deal_state: GameStateSchema = GameStateSchema(
                user=BaseUserSchema(user_id=user_id, username=seat.user.user.username),
                cards=cards,  # Передаем список карт вместо одной карты
            )
            # Выполняем команду добавления пачки карт
            game = await AddUserCardFromDeckCommand().execute(
                request=deal_state, game=game, room=room
            )

        return game
