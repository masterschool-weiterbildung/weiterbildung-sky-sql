RESULT = "result"
MESSAGE = "message"
PAYLOAD = "payload"


def result_message(result: bool, message: str, result_set) -> dict:
    return {
        RESULT: result,
        MESSAGE: message,
        PAYLOAD: result_set
    }
