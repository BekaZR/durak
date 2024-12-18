from abc import ABC

from domain.attack.command import AttackCommand


class AttackStrategy(ABC):
    GAME_COMMANDS = []
    SUPPORT_COMMANDS = []


class FirstAttackStrategy(AttackStrategy):
    GAME_COMMANDS = [
        AttackCommand,
    ]
    SUPPORT_COMMANDS = []
