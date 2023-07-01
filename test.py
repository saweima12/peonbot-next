import re
from opencc import OpenCC

BLOCK_ARABI =  re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF]')
def check_arabi(text: str) -> bool:
    result = re.match(BLOCK_ARABI, text)

    if result:
        return True
    return False    

print(check_arabi("wwweee"))