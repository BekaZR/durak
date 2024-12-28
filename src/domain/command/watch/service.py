from db.models.room import Room
from domain.command.timer.service import TimerService
from domain.command.game.schema import GameOutSchema, GameSchema
from domain.command.user.schema import UserOutSchema
from domain.command.seat.schema import SeatOutSchema
from domain.command.timer.schema import TimerCreateSchema


class WatchService:
    def __init__(self) -> None:
        self.timer_service = TimerService()

    async def get_game_state(self, game: GameSchema, room: Room) -> GameOutSchema:
        # Преобразуем игровое состояние для наблюдателей
        game_out_schema = GameOutSchema(
            seats={},
            round=game.round,
            deck=game.deck,
            turn=game.turn,
            status=game.status,
            trump=game.trump,
        )

        # Заполняем информацию о местах
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

        return game_out_schema

    async def get_timers(self, room_id: int) -> list[TimerCreateSchema]:
        # Получаем все активные таймеры для комнаты
        return await self.timer_service.get_all_timer(room_id)
