
class CustomException(Exception):
    def __init__(self, *args: object, msg: str, ) -> None:
        super().__init__(*args);
        self.msg = msg;
