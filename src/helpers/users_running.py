class UsersRunning:
    def __init__(self) -> None:
        self.__users_running: set[str] = set()

    @property
    def users_running_list(self) -> list[str]:
        return list(self.__users_running)

    def add_new_user_running(self, author_id: str) -> None:
        if author_id in self.__users_running:
            raise ValueError(f"{author_id} is already in users_running")
        self.__users_running.add(author_id)

    def remove_user_running(self, author_id: str) -> None:
        if author_id not in self.__users_running:
            raise ValueError(f"{author_id} is not in users_running")
        self.__users_running.remove(author_id)
