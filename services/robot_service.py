import asyncio
import random
from enum import Enum


class RobotPosition(int, Enum):
    MOVING = 0
    BASE_1 = 1
    BASE_2 = 2
    BASE_3 = 3


class RobotService:
    def __init__(self) -> None:
        self._current_position = RobotPosition.BASE_1
        self._is_moving = False
        self._lock = asyncio.Lock()

    async def get_current_position(self) -> dict:
        async with self._lock:
            return {
                "position": self._current_position.value,
                "position_name": self._current_position.name,
                "is_moving": self._is_moving,
            }

    async def move_to_next_base(self) -> dict:
        async with self._lock:
            if self._is_moving:
                return {"error": "El robot ya se está moviendo"}

            previus_position = self._current_position

            self._is_moving = True
            self._current_position = RobotPosition.MOVING

            if previus_position == RobotPosition.BASE_3:
                next_position = RobotPosition.BASE_1
            else:
                next_position = RobotPosition(previus_position.value + 1)

            asyncio.create_task(self._simulate_movement(next_position))

            return {
                "message": f"Robot en movimiento hacia {next_position.name}",
                "next_position": next_position.value,
                "estimated_time": "hasta 30 segundos"
            }

    async def _simulate_movement(self, target_position: RobotPosition):
        move_time = random.randint(10, 30)

        await asyncio.sleep(move_time)

        async with self._lock:
            self._current_position = target_position
            self._is_moving = False

robot_service = RobotService()
