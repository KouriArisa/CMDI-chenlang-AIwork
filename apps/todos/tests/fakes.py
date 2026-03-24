class FakeTodoService:
    def __init__(self) -> None:
        self.list_called = False

    def list_todos(self, *, query):
        self.list_called = True
        return []

    def get_todo(self, *, todo_id: int):
        raise NotImplementedError

    def create_todo(self, *, payload):
        raise NotImplementedError

    def update_todo(self, *, todo_id: int, payload):
        raise NotImplementedError

    def delete_todo(self, *, todo_id: int):
        raise NotImplementedError

    def toggle_status(self, *, todo_id: int):
        raise NotImplementedError
