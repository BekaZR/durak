from domain.command.slot.schema import SlotOutSchema


class SlotService:
    async def get_all_slots_status(self, slots: list[SlotOutSchema]) -> list[bool]:
        return [slot.status for slot in slots]

    async def get_free_slots(self, slots: list[SlotOutSchema]) -> list[SlotOutSchema]:
        return [slot for slot in slots if not slot.status]

    async def is_maximum_slots(
        self, slots: list[SlotOutSchema], is_fisrt_round: bool
    ) -> bool:
        """
        Checks if the current round has reached the maximum number of slots.
        If the round has beats, the maximum is 6 slots, otherwise it is 5.
        If the maximum is reached, sends an error message to the sender's websocket.
        """
        if not is_fisrt_round:
            max_slots = 6
        else:
            max_slots = 5
        if len(slots) >= max_slots:
            return True
        return False
