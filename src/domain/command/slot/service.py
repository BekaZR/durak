from domain.command.slot.schema import SlotOutSchema


class SlotService:
    async def get_all_slots_status(self, slots: list[SlotOutSchema]) -> list[bool]:
        return [slot.status for slot in slots]

    async def get_free_slots(self, slots: list[SlotOutSchema]) -> list[SlotOutSchema]:
        return [slot for slot in slots if not slot.status]
