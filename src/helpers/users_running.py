class UsersRunning:
    def __init__(self) -> None:
        self.__users_running = []

    @property
    def users_running_list(self) -> list:
        return self.__users_running

    def add_new_user_running(self, author_id: str) -> None:
        self.__users_running.append(author_id)

    def remove_user_running(self, author_id: str) -> None:
        if not self.__is_author_id_in_users_running(author_id):
            raise ValueError(f"{author_id} is not in users_running")
        self.__users_running.remove(author_id)

    def __is_author_id_in_users_running(self, author_id: str) -> bool:
        return author_id in self.__users_running
