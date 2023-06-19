import re
from opencc import OpenCC


BLOCK_PTN = r"(群增粉|僵尸|[群私代贷].*[发蕟發]|[广廣].*告|[炒炸进進]群|[买卖].*(号|飞机|会员|在线|支付宝|微信|抖音)|号商|(电报|Telegram|TG|飞机|会员|在线).?.?([代秒]开|开[户号]|店)|([代秒]开|开[户号]).?.?(飞机|会员|在线)|引流|跑[分芬]|[收出回黑盗][uU]|[uU]商|下浮[uU]|[uU].?[sS].?[dD].?[tT]|哈[希稀]|手续费|返佣|共富|国际娱乐|娱乐客服|[賭赌][场場博]|博[彩采]|棋牌|赚钱.*(一定|要看).*项目|[喊带帶][单單]|招商|搭建|远控|免[费費]|翻墙|免.*(梯子|[vV][pP][nN])|(网络|专线).*接入|[视視][频頻]|吞精|[幼呦喲稚].?.?[女幼呦喲裙童龄]|[蘿萝]莉|[破坡].?.?[处處]|[资資]源|[找私絲斯].*我|[资資姿U][源原U].*我|[资咨征询问讯联系接洽][资咨征询问讯联系接洽]我|[点點][击擊我]|[看点點].*([头頭][像貼贴]|照片|[頻频]道)|[加\+].*line|\+.*賴|(中文|电报).*(\(tg\)|telegram|电报)|(address|Contract))"
def check_block_name(text: str):
    result = re.search(BLOCK_PTN, text)

    if result:
        return True
    return False

def check_str(text: str) -> bool:
    # fetch all chinese word.
    converter = OpenCC("s2t")
    words = re.findall(r"([^u4E00-u9FA5])", text)
    origin_str = "".join(words).strip()
    tc_str = converter.convert(origin_str)
    point = 0
    for index, value in enumerate(tc_str):
        if value != origin_str[index]:
            point += 1

            print(value)
            if point >= 1:
                break