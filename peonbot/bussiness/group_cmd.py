from peonbot.extension.command import CommandMap

from .commands import (
    group_point,
    group_start
)

group_cmd_map = CommandMap(prefix="$")
group_cmd_map.register_command_handler("point", group_point.process)
group_cmd_map.register_command_handler("start", group_start.process)