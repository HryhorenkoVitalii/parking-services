from entities import PermissionPriorities, Permissions
from collections import defaultdict

PRIORITIES_QUEUE = PermissionPriorities(
    first_priorities=[Permissions.vip_permission,
                      Permissions.permission1,],
    second_priorities=[Permissions.permission2],
    thirst_priorities=[Permissions.permission3]
    )

class ParkingNode:
    __slots__ = ["number_place", "car_number", "permission"]
    
    def __init__(self, 
                 number_place: int, 
                 car_number: str | None = None, 
                 permission: Permissions | None= None):
        self.number_place:int = number_place
        self.car_number:str | None = car_number
        self.permission: Permissions | None  = permission
    
    @property
    def is_empty(self) -> bool:
        if self.car_number:
            return False
        return True
    
    def get_node(self, car_number: str) -> int:
        self.car_number = car_number
        return self.number_place
    
    def clean_node(self)-> None:
        self.car_number = None
    
    
class Parking:
    __slots__ = ["regular_nodes", "permission_nodes", "occupied_nodes"]
    
    def __init__(self):
        self.regular_nodes: list[ParkingNode] = []
        self.permission_nodes: list[ParkingNode] = []
        self.occupied_nodes: list[ParkingNode] =  []

    @property
    def get_empty_count(self) -> dict[str, int]:
        count_nodes: dict[str, int]  = defaultdict(int)
        for node in self.permission_nodes:
            count_nodes[node.permission.value] += 1
        count_nodes["regular"] = len(self.regular_nodes)
        return count_nodes
    
    def car_come(self, car_number: str, permission: Permissions | None = None) -> int or False:
        if permission:
            available_priority = self._get_available_priority(permission)
            for node in self.permission_nodes:
                if node.permission in available_priority:
                    self.occupied_nodes.append(node)
                    self.permission_nodes.remove(node)
                    return node.get_node(car_number)
    
        for node in self.regular_nodes:
            self.occupied_nodes.append(node)
            self.regular_nodes.remove(node)
            return node.get_node(car_number)

        return False # if all nodes in occupied

    def car_leave(self, car_number: str) -> bool:
        for node in self.occupied_nodes:
            if node.car_number == car_number:
                node.clean_node
                if node.is_regular:
                    self.regular_nodes.append(node)
                else:
                    self.permission_nodes.append(node)
                self.occupied_nodes.remove(node)
                return True
            return False # if car_number dont found

    def _get_available_priority(self, permission: Permissions) -> list[ParkingNode]:
        available_permission = []
        for permissions in reversed(PRIORITIES_QUEUE):
            available_permission.extend(permissions)
            if permission in permissions:
                return available_permission
