import asyncio
import random
from enum import Enum

from yamaha_bot_backend.services.logger_service import robot_logger


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
        robot_logger.info(
            "Servicio de robot inicializado", 
            {"initial_position": "BASE_1", "initial_state": "stopped"}
        )

    async def get_current_position(self) -> dict:
        async with self._lock:
            position_data = {
                "position": self._current_position.value,
                "position_name": self._current_position.name,
                "is_moving": self._is_moving,
            }
            robot_logger.debug(
                "Consulta de posición del robot",
                position_data
            )
            return position_data

    async def move_to_next_base(self) -> dict:
        async with self._lock:
            if self._is_moving:
                robot_logger.warning(
                    "Intento de mover robot mientras ya está en movimiento",
                    {"current_position": self._current_position.name}
                )
                return {"error": "El robot ya se está moviendo"}

            previous_position = self._current_position

            self._is_moving = True
            self._current_position = RobotPosition.MOVING

            if previous_position == RobotPosition.BASE_3:
                next_position = RobotPosition.BASE_1
            else:
                next_position = RobotPosition(previous_position.value + 1)

            # Log del movimiento iniciado
            robot_logger.info(
                "Movimiento del robot iniciado",
                {
                    "from_position": previous_position.name,
                    "to_position": next_position.name,
                    "from_value": previous_position.value,
                    "to_value": next_position.value,
                    "estimated_time_seconds": "10-30"
                }
            )

            asyncio.create_task(self._simulate_movement(next_position))

            return {
                "message": f"Robot en movimiento hacia {next_position.name}",
                "next_position": next_position.value,
                "estimated_time": "hasta 30 segundos"
            }

    async def _simulate_movement(self, target_position: RobotPosition):
        move_time = random.randint(10, 30)
        
        robot_logger.debug(
            "Simulando movimiento del robot",
            {
                "target_position": target_position.name,
                "move_time_seconds": move_time,
                "target_value": target_position.value
            }
        )

        await asyncio.sleep(move_time)

        async with self._lock:
            self._current_position = target_position
            self._is_moving = False
            
            robot_logger.info(
                "Movimiento del robot completado",
                {
                    "final_position": target_position.name,
                    "final_value": target_position.value,
                    "movement_time_seconds": move_time,
                    "new_state": "stopped"
                }
            )

    async def set_position_directly(self, position: int) -> dict:
        """Establece la posición directamente (para testing/debug)"""
        async with self._lock:
            try:
                old_position = self._current_position
                self._current_position = RobotPosition(position)
                self._is_moving = False
                
                robot_logger.info(
                    "Posición del robot establecida manualmente",
                    {
                        "old_position": old_position.name,
                        "new_position": self._current_position.name,
                        "old_value": old_position.value,
                        "new_value": position,
                        "reason": "manual_override"
                    }
                )
                
                return {
                    "message": f"Posición establecida a {self._current_position.name}",
                    "position": self._current_position.value
                }
            except ValueError:
                robot_logger.error(
                    "Intento de establecer posición inválida",
                    {"invalid_position": position}
                )
                return {"error": f"Posición inválida: {position}"}


robot_service = RobotService()