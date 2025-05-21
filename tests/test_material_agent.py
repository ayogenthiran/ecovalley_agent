import pytest
from src.agents.material_agent import MaterialSelectionAgent

@pytest.fixture
def material_agent():
    return MaterialSelectionAgent()

@pytest.mark.asyncio
async def test_material_agent_validation(material_agent):
    # Test valid input
    valid_input = {
        "product_type": "sustainable packaging",
        "requirements": "biodegradable, lightweight"
    }
    assert await material_agent.validate(valid_input) is True
    
    # Test invalid input
    invalid_input = {
        "product_type": "sustainable packaging"
    }
    assert await material_agent.validate(invalid_input) is False

@pytest.mark.asyncio
async def test_material_agent_process():
    agent = MaterialSelectionAgent()
    input_data = {
        "product_type": "sustainable packaging",
        "requirements": "biodegradable, lightweight"
    }
    
    result = await agent.process(input_data)
    
    assert "materials" in result
    assert "reasoning" in result
    assert isinstance(result["materials"], list)
    assert isinstance(result["reasoning"], str) 