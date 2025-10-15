import pytest
import asyncio
from unittest.mock import patch

from yamaha_bot_backend.services.robot_service import RobotService, RobotPosition


class TestRobotService:
    @pytest.mark.asyncio
    async def test_initial_position(self, robot_service):
        position = await robot_service.get_current_position()
        assert position["position"] == RobotPosition.BASE_1.value
        assert position["is_moving"] is False

    @pytest.mark.asyncio
    async def test_move_from_base1_to_base2(self, robot_service):
        result = await robot_service.move_to_next_base()
        
        # Assert movimiento iniciado
        assert "en movimiento" in result["message"]
        assert result["next_position"] == RobotPosition.BASE_2.value
        
        # Verificar estado durante movimiento
        position = await robot_service.get_current_position()
        assert position["position"] == RobotPosition.MOVING.value
        assert position["is_moving"] is True

    @pytest.mark.asyncio
    async def test_move_from_base3_to_base1(self, robot_service):
        # Arrange - establecer en BASE_3
        await robot_service.set_position_directly(RobotPosition.BASE_3.value)
        
        result = await robot_service.move_to_next_base()
        
        # Assert
        assert result["next_position"] == RobotPosition.BASE_1.value

    @pytest.mark.asyncio
    async def test_cannot_move_while_moving(self, robot_service):
        # Primer movimiento
        await robot_service.move_to_next_base()
        
        # Intentar segundo movimiento
        result = await robot_service.move_to_next_base()
        
        assert "error" in result
        assert "ya se está moviendo" in result["error"]

    @pytest.mark.asyncio
    async def test_simulate_movement_completion(self, robot_service):
        # Usar tiempo muy corto para prueba
        with patch('random.randint', return_value=0.1):
            # Iniciar movimiento
            await robot_service.move_to_next_base()
            
            # Esperar a que termine el movimiento
            await asyncio.sleep(0.2)
            
            # Verificar que llegó a la posición destino
            position = await robot_service.get_current_position()
            assert position["position"] == RobotPosition.BASE_2.value
            assert position["is_moving"] is False
