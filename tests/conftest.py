# tests/conftest.py
import pytest
from domain.command.seat.schema import SeatSchema
from domain.command.user.schema import UserSchema, UserAchieved, BaseUserSchema
from domain.command.turn.service import TurnService
from domain.command.card.schema import CardSchema


@pytest.fixture
def turn_service() -> TurnService:
    return TurnService()


@pytest.fixture
def sample_seats() -> dict[int, SeatSchema]:
    """Creates a sample game state with 4 players"""
    seats = {}
    for i in range(4):
        seats[i] = SeatSchema(
            user=UserSchema(
                user=BaseUserSchema(user_id=i, username=f"Player{i}"),
                cards=[],
                achieved=UserAchieved.PROCESSING,
            ),
            position=i,
        )
    return seats


@pytest.fixture
def sample_cards() -> list[CardSchema]:
    """Sample cards for testing"""
    return [
        CardSchema(rank="A", suit="hearts"),
        CardSchema(rank="K", suit="diamonds"),
        CardSchema(rank="Q", suit="clubs"),
    ]
