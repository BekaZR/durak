import asyncio
from datetime import datetime


# Подход 2: Через аргумент
class Command:
    async def execute(self, delay: int = 0) -> None:
        if delay:
            await asyncio.sleep(delay)
        print(f"Executed at {datetime.now()}")


async def main() -> None:
    print(f"Starting at {datetime.now()}\n")

    # Подход 1: С декоратором
    print("Using decorator:")
    # await decorated_command()
    asyncio.create_task(Command().execute())
    await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
