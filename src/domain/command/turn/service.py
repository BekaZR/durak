from domain.command.seat.schema import SeatSchema
from domain.command.turn.schema import TurnSchema
from domain.command.user.schema import UserAchieved
from domain.command.user.types import UserID


class TurnService:
    def create_all_players_queue(
        self, seats: dict[UserID, SeatSchema], attacker_id: UserID
    ) -> TurnSchema:
        """Создает очередь где подкидывать могут все игроки"""
        # Находим защищающегося
        defender_id = self._get_next_player(seats, attacker_id)

        # Все игроки кроме атакующего и защищающегося
        queue = [
            user_id
            for user_id, seat in seats.items()
            if seat.user.achieved == UserAchieved.PROCESSING
            and user_id not in (attacker_id, defender_id)
        ]
        # Сортируем по позициям
        queue.sort(key=lambda x: seats[x].position)

        return TurnSchema(
            currenct_attacker_user_id=attacker_id,
            current_defender_user_id=defender_id,
            queue=queue,
        )

    def create_neighbors_queue(
        self, seats: dict[UserID, SeatSchema], attacker_id: UserID
    ) -> TurnSchema:
        """Создает очередь где подкидывать могут только соседи"""
        # Находим защищающегося
        defender_id = self._get_next_player(seats, attacker_id)

        # Находим соседние позиции атакующего
        attacker_position = seats[attacker_id].position
        max_position = max(seat.position for seat in seats.values())
        prev_pos = attacker_position - 1 if attacker_position > 0 else max_position
        next_pos = attacker_position + 1 if attacker_position < max_position else 0

        # Формируем очередь из соседей
        queue = [
            user_id
            for user_id, seat in seats.items()
            if seat.position in (prev_pos, next_pos)
            and seat.user.achieved == UserAchieved.PROCESSING
            and user_id != defender_id
        ]

        return TurnSchema(
            currenct_attacker_user_id=attacker_id,
            current_defender_user_id=defender_id,
            queue=queue,
        )

    def _get_next_player(
        self, seats: dict[UserID, SeatSchema], current_player_id: UserID
    ) -> UserID:
        """Получить следующего игрока по кругу"""
        current_position = seats[current_player_id].position
        max_position = max(seat.position for seat in seats.values())
        next_position = (current_position + 1) if current_position < max_position else 0

        return next(
            user_id
            for user_id, seat in seats.items()
            if seat.position == next_position
            and seat.user.achieved == UserAchieved.PROCESSING
        )
