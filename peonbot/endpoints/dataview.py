from sanic import Sanic, Request, Blueprint, response
from peonbot import textlang
from peonbot.common.bot import get_bot
from peonbot.bussiness.services import DataViewService
from peonbot.utils.bot_util import get_bot_token

def register(app: Sanic) -> Blueprint:

    bp = Blueprint(name="dataview", url_prefix="/dataview")

    service = DataViewService()

    bot = get_bot(app)

    @bp.get("/chats")
    async def get_chats(_: Request):
        data = await service.get_avaliable_chats()

        if not data:
            return response.empty(404)

        result = [{
            'chat_id': item.chat_id,
            'chat_name': item.chat_name,
        } for item in data]

        return response.json(result)

    @bp.get("/chats/<chat_id>")
    async def get_chat(_: Request, chat_id: str):
        data = await service.get_chat_by_id(chat_id)

        if not data:
            return response.empty(404)
        
        result = {
            'chat_id': data.chat_id,
            'chat_name': data.chat_name
        }
        return response.json(result)

    @bp.get("/chats/<chat_id>/members")
    async def get_members(_: Request, chat_id: str):

        data = await service.get_member_data(chat_id)

        if not data:
            return response.empty(404)

        result = [ {
            "full_name": item.full_name,
            "point": item.msg_count,
            "last_updated": item.update_time.isoformat()
        } for item in data]

        return response.json(result)


    @bp.get("/chats/<chat_id>/deletedmsg")
    async def get_delete_msg_list(_: Request, chat_id: str):
        data = await service.get_deleted_message(chat_id)

        if not data:
            return response.empty(404)

        result = []
        for item in data:
            full_name = service.get_full_name(item.message_json)
            user_id = service.get_user_id(item.message_json)
            username = service.get_username(item.message_json)
            raw = service.format_delete_msg(item.message_json)

            result.append({
                'content_type': item.content_type,
                'raw': raw,
                'full_name': full_name,
                'user_id': user_id,
                'username': username,
                'record_time': item.record_date.isoformat()
            })

        return response.json(result)


    @bp.get("/<token:str>/send_tips")
    async def send_dataview_tips(request: Request, token: str):

        if token != get_bot_token(request.app):
            return response.empty(200)

        chats = await service.get_avaliable_chats()

        for item in chats:
            chat_id = item.chat_id
            result = await service.get_deleted_context(chat_id)

            # get data from result.
            senders = result.get("senders")
            count = result.get("count")

            # generate tips message
            sender_str = "\n".join([
                textlang.SENDER_PTN.format(fullname=fullname, user_id=user_id)
                for user_id, fullname in senders
            ])
            url_str = textlang.URL_PTN.format(chat_id=chat_id)
            text = textlang.TIPS_DAILY_TIPS.format(count=count, url=url_str, senders=sender_str)

            app.add_task(bot.send_message(chat_id, text, parse_mode='markdown'))

        return response.empty(200)

    return bp
