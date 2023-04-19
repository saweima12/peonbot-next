import re

def check_has_url(text: str):
    URL_PTN = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
    result = re.match(URL_PTN, text)

    if result:
        return True
    return False


def parse_int(text: str) -> int | None:
    try:
        return int(text)
    except Exception:
        return None
