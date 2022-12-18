from typing import NamedTuple
from enum import Enum

class Permissions(Enum):
    vipv_permission = "vip_permission"
    permission1 = "permission1"
    permission2 = "permission2"
    permission3 = "permission3"


class PermissionPriorities(NamedTuple):
    first_priorities: list(Permissions)
    second_priorities: list(Permissions)
    thirst_priorities: list(Permissions) 
