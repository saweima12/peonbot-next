from sanic import Request, Blueprint

bp = Blueprint(name="dataview", url_prefix="/dataview")


@bp.get("/chats")
async def get_chats(request: Request):
    pass

@bp.get("/chats/<id>/members")
async def get_members(request: Request, id: str):
    pass

@bp.get("/chats/<id>/delete_msg")
async def get_delete_msg_list(request: Request, id: str):
    pass