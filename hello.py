from typing import NewType, Annotated


UserID = NewType("UserID", int)
UserID2 = Annotated[int, "UserID"]


def main(user_id: UserID2) -> None:
    print(user_id)
    return


if __name__ == "__main__":
    main(2)
