from sanic import Sanic, Request, Blueprint, response
from peonbot.bussiness.services import DataViewService


def register(_: Sanic) -> Blueprint:

    bp = Blueprint(name="dataview", url_prefix="/dataview")

    service = DataViewService()

    @bp.get("/chats")
    async def get_chats(_: Request):
        result = await service.get_chats()

        if not result:
            return response.empty(404)

        return response.json(result)


    @bp.get("/chats/<chat_id>/members")
    async def get_members(_: Request, chat_id: str):

        result = await service.get_member_data(chat_id)

        if not result:
            return response.empty(404)

        return response.json(result)


    @bp.get("/chats/<chat_id>/deleted_msg")
    async def get_delete_msg_list(_: Request, chat_id: str):

        result = await service.get_deleted_message(chat_id)

        if not result:
            return response.empty(404)

        return response.json(result)

    return bp
