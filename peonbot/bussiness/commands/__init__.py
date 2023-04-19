from peonbot.common.command import CommandMap

from .point import PointCmd
from .setlevel import SetLevelCmd
from .save import SaveCmd

def register(cmd_map: CommandMap, service_map: dict):

    point_cmd = PointCmd(**service_map)
    cmd_map.register_command("point", point_cmd)

    setlevel_cmd = SetLevelCmd(**service_map)
    cmd_map.register_command("setlevel", setlevel_cmd)

    save_cmd = SaveCmd()
    cmd_map.register_command("save", save_cmd)
