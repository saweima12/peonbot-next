import re

URL_PTN = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"

def check_has_url(text: str):
    result = re.match(URL_PTN, text)

    if result:
        return True
    return False

BLOCK_PTN = r"(群增粉|僵尸|[群私代贷].*[发蕟發]|[广廣].*告|[炒炸进進]群|[买卖].*(号|飞机|会员|在线|支付宝|微信|抖音)|号商|(电报|Telegram|TG|飞机|会员|在线).?.?([代秒]开|开[户号]|店)|([代秒]开|开[户号]).?.?(飞机|会员|在线)|引流|跑[分芬]|[收出回黑盗][uU]|[uU]商|下浮[uU]|[uU].?[sS].?[dD].?[tT]|哈[希稀]|手续费|返佣|共富|国际娱乐|娱乐客服|[賭赌][场場博]|博[彩采]|棋牌|赚钱.*(一定|要看).*项目|[喊带帶][单單]|招商|搭建|远控|免[费費]|翻墙|免.*(梯子|[vV][pP][nN])|(网络|专线).*接入|[视視][频頻]|吞精|[幼呦喲稚].?.?[女幼呦喲裙童龄]|[蘿萝]莉|[破坡].?.?[处處]|[资資]源|[找私絲斯].*我|[资資姿U][源原U].*我|[资咨征询问讯联系接洽][资咨征询问讯联系接洽]我|[点點][击擊我]|[看点點].*([头頭][像貼贴]|照片|[頻频]道)|[加\+].*line|\+.*賴|(中文|电报).*(\(tg\)|telegram|电报)|(address|Contract)\:0x"

def check_block_name(text: str):
    result = re.match(BLOCK_PTN, text)

    if result:
        return True
    return False


def parse_int(text: str) -> int | None:
    try:
        return int(text)
    except Exception:
        return None
