from typing import NamedTuple
from enum import Enum

class Permissions(Enum):
    vip_permission = "vip_permission"
    permission1 = "permission1"
    permission2 = "permission2"
    permission3 = "permission3"
    
    
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 


class PermissionPriorities(NamedTuple):
    first_priorities: list(Permissions)
    second_priorities: list(Permissions)
    thirst_priorities: list(Permissions) 
