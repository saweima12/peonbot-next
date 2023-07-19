from aiogram import Bot
from sanic.log import logger
from peonbot.textlang import SENDER_PTN, TIPS_QUERY_FAILED, TIPS_QUERY_SUCCESS
from peonbot.common.command import AbstractCommand
from peonbot.models.context import MessageContext
from peonbot.extensions.helper import MessageHelper

class QueryCmd(AbstractCommand):

    def __init__(self, bot: Bot, **_):
        self.bot = bot

    async def run(self, *args, helper: MessageHelper, ctx: MessageContext, **kwargs):
        if not ctx.is_admin and not ctx.is_whitelist:
            return
        
        if len(args) < 1:
            return
        
        query_str = " ".join(args)
        members_str = []
        for member_id in args:
            try:
                member = await self.bot.get_chat_member(helper.chat_id, member_id)
                members_str.append(SENDER_PTN.format(fullname=member.user.full_name, user_id=member_id))               
            except:
                logger.warn(f"User not found, id: {member_id}")
            
        if not members_str:
            _tips = self.bot.send_message(helper.chat_id, TIPS_QUERY_FAILED, parse_mode='markdown')
            logger.info("Query failed, users not found.")  
            return
        
        try:
            _content = "\n".join(members_str)
            # send user's mention
            _msg = TIPS_QUERY_SUCCESS.format(content=_content, count=len(members_str))
            await helper.bot.send_message(helper.chat_id, _msg, parse_mode='markdown')
            logger.info(f"User {helper.user.full_name} query member_id {query_str}")
        
        except Exception as _e:
            logger.error(_e)
