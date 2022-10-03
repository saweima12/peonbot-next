from peonbot.extension.msg_helper import MessageHelper


async def process(*params, helper: MessageHelper, **options):
    print(helper)