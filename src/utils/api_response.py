class BaseResponse:
    def __init__(self, msg: str = "", code: int = 200, data: any = {}, error: str = "", errorCode: int = 0) -> None:
        self.msg = msg
        self.code = code
        self.data = data
        self.error = error
        self.errorCode = errorCode

    def __dict__(self) -> dict:
        return {}


class SuccessResponse(BaseResponse):
    def __init__(self, msg: str = "", code: int = 200, data: any = {}, error: str = "") -> None:
        super().__init__(msg, code, data, error)

    def __dict__(self) -> dict:
        return {
            "msg": self.msg,
            "code": self.code,
            "data": self.data
        }


class ErrorResponse(BaseResponse):
    def __init__(self, msg: str = "", code: int = 500, data: any = {}, error: str = "Something went wrong.", errorCode: int = 0) -> None:
        super().__init__(msg, code, data, error, errorCode)

    def __dict__(self) -> dict:
        return {
            "code": self.code,
            "error": self.error,
            "error_code": self.errorCode
        }
