from peonbot.extension.helper import MessageHelper


async def process(*params, helper: MessageHelper, **options):
    print(helper)