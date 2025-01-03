from domain.command.seat.schema import SeatSchema
from domain.command.turn.exception import NeigborsNotExistError
from domain.command.turn.schema import TurnSchema
from domain.command.user.schema import UserAchieved
from domain.command.user.types import UserID


class TurnService:
    def _get_active_positions(self, seats: dict[UserID, SeatSchema]) -> list[int]:
        # Get positions of active players
        return sorted(
            [
                seat.position
                for seat in seats.values()
                if seat.user.achieved == UserAchieved.PROCESSING
            ]
        )

    def _get_next_position(self, current_pos: int, positions: list[int]) -> int:
        current_idx = positions.index(current_pos)
        return positions[(current_idx + 1) % len(positions)]

    def create_neighbors_queue(
        self, attacker_id: UserID, seats: dict[UserID, SeatSchema]
    ) -> TurnSchema:
        position_to_id = {seat.position: uid for uid, seat in seats.items()}
        active_positions = self._get_active_positions(seats)

        attacker_pos = seats[attacker_id].position
        defender_pos = self._get_next_position(attacker_pos, active_positions)
        next_pos = self._get_next_position(defender_pos, active_positions)
        if next_pos == attacker_pos:
            queue = [position_to_id[next_pos]]
        else:
            queue = [attacker_id, position_to_id[next_pos]]
        return TurnSchema(
            currenct_attacker_user_id=attacker_id,
            current_defender_user_id=position_to_id[defender_pos],
            queue=queue,
            neigbor_user_id=position_to_id[next_pos],
        )

    def create_all_players_queue(
        self, attacker_id: UserID, seats: dict[UserID, SeatSchema]
    ) -> TurnSchema:
        position_to_id = {seat.position: uid for uid, seat in seats.items()}
        active_positions = self._get_active_positions(seats)

        attacker_pos = seats[attacker_id].position
        defender_pos = self._get_next_position(attacker_pos, active_positions)

        # Start building queue from position after defender
        current_pos = defender_pos
        queue = [attacker_id]

        while True:
            current_pos = self._get_next_position(current_pos, active_positions)
            if current_pos == attacker_pos:
                break
            queue.append(position_to_id[current_pos])

        return TurnSchema(
            currenct_attacker_user_id=attacker_id,
            current_defender_user_id=position_to_id[defender_pos],
            queue=queue,
        )

    def find_next_attacker_after_defense(
        self, current_turn: TurnSchema, seats: dict[UserID, SeatSchema]
    ) -> UserID:
        """
        Find the next attacker for the following round.

        Args:
            current_turn: Current turn state with attacker, defender and queue
            seats: Dictionary of all seats with player states

        Returns:
            UserID of the next attacker
        """

        # who hasn't won/lost yet (is still PROCESSING)
        defender_id = current_turn.current_defender_user_id
        if seats[defender_id].user.achieved == UserAchieved.PROCESSING:
            return defender_id

        # If defender won, find next PROCESSING player
        position_to_id = {seat.position: uid for uid, seat in seats.items()}
        all_positions = sorted([seat.position for seat in seats.values()])
        defender_pos = seats[defender_id].position

        current_pos = defender_pos
        while True:
            current_pos = self._get_next_position(current_pos, all_positions)
            current_id = position_to_id[current_pos]
            if seats[current_id].user.achieved == UserAchieved.PROCESSING:
                return current_id

            if current_pos == defender_pos:
                return defender_id

    def find_next_attacker_after_take(
        self, current_turn: TurnSchema, seats: dict[UserID, SeatSchema]
    ) -> UserID:
        """
        Find the next attacker for the following round.

        Args:
            current_turn: Current turn state with attacker, defender and queue
            seats: Dictionary of all seats with player states

        Returns:
            UserID of the next attacker
        """

        # who hasn't won/lost yet (is still PROCESSING)
        position_to_id = {seat.position: uid for uid, seat in seats.items()}
        all_positions = sorted([seat.position for seat in seats.values()])
        defender_pos = seats[current_turn.current_defender_user_id].position

        # Start checking from position after defender
        current_pos = defender_pos
        while True:
            current_pos = self._get_next_position(current_pos, all_positions)
            current_id = position_to_id[current_pos]
            if seats[current_id].user.achieved == UserAchieved.PROCESSING:
                return current_id

            # If we've checked all positions and found no PROCESSING players,
            # the game should be over, but we'll return defender as fallback
            if current_pos == defender_pos:
                return current_turn.current_defender_user_id

    # Current Implementation Analysis

    async def restore_turn_system_all_players(
        self, current_turn: TurnSchema, seats: dict[UserID, SeatSchema]
    ) -> TurnSchema:
        """
        Восстанавливает очередь для всех игроков после успешной защиты.
        Очередь должна начинаться с текущего первого игрока в очереди.
        """
        position_to_id = {seat.position: uid for uid, seat in seats.items()}
        id_to_position = {uid: seat.position for uid, seat in seats.items()}
        active_positions = self._get_active_positions(seats)

        # Проверяем текущих активных игроков
        active_players = {
            uid
            for uid, seat in seats.items()
            if seat.user.achieved == UserAchieved.PROCESSING
            and uid != current_turn.current_defender_user_id
        }

        # Определяем начальную позицию для новой очереди
        if current_turn.queue:
            # Если очередь не пуста, начинаем с первого игрока в текущей очереди
            current_id = current_turn.queue[0]
        else:
            # Если очередь пуста, начинаем с текущего атакующего
            current_id = current_turn.currenct_attacker_user_id

        # Собираем новую очередь, сохраняя порядок
        new_queue = []
        current_pos = id_to_position[current_id]
        seen_positions = {current_pos}

        while True:
            if position_to_id[current_pos] in active_players:
                new_queue.append(position_to_id[current_pos])

            current_pos = self._get_next_position(current_pos, active_positions)
            if current_pos in seen_positions:
                break
            seen_positions.add(current_pos)

        return TurnSchema(
            currenct_attacker_user_id=current_turn.currenct_attacker_user_id,
            current_defender_user_id=current_turn.current_defender_user_id,
            neigbor_user_id=None,
            queue=new_queue,
        )

    async def restore_turn_system_neighbors(
        self, current_turn: TurnSchema, seats: dict[UserID, SeatSchema]
    ) -> TurnSchema:
        """
        Восстанавливает очередь для соседей после успешной защиты.
        Если сосед выбыл из игры, в очереди остается только исходный атакующий.
        """
        queue = []
        if current_turn.neigbor_user_id is None:
            raise NeigborsNotExistError()
        # Если сосед все еще в игре, добавляем его и атакующего
        if seats[current_turn.neigbor_user_id].user.achieved == UserAchieved.PROCESSING:
            queue = [
                current_turn.neigbor_user_id,
                current_turn.currenct_attacker_user_id,
            ]
        # Если сосед выбыл, добавляем только атакующего
        elif (
            seats[current_turn.currenct_attacker_user_id].user.achieved
            == UserAchieved.PROCESSING
        ):
            queue = [current_turn.currenct_attacker_user_id]

        return TurnSchema(
            currenct_attacker_user_id=current_turn.currenct_attacker_user_id,
            current_defender_user_id=current_turn.current_defender_user_id,
            neigbor_user_id=current_turn.neigbor_user_id,
            queue=queue,
        )
