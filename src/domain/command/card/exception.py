from exception.base import BackendError


class TrumpNotExist(BackendError):
    code = "trump_not_exist"
    description = "Trump does not exist"


class DeckEmptyError(BackendError):
    code = "deck_empty"
    description = "Deck is empty"


class CardNotInHandError(BackendError):
    code = "card_not_in_hand"
    description = "Card not in hand"


class CardNotInTableError(BackendError):
    code = "card_not_in_table"
    description = "Card not in table"
