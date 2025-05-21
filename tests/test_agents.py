import pytest
import asyncio
from src.agents.base_agent import BaseAgent
from src.agents.recommendation_agent import RecommendationAgent
from src.agents.environmental_impact_agent import EnvironmentalImpactAgent
from src.agents.cost_analysis_agent import CostAnalysisAgent
from src.agents.material_selection_agent import MaterialSelectionAgent

@pytest.mark.asyncio
async def test_environmental_impact_agent_valid():
    agent = EnvironmentalImpactAgent()
    input_data = {
        "materials": ["Bamboo", "Hemp"],
        "quantities": [100, 200]
    }
    result = await agent.process(input_data)
    assert "direct_impacts" in result
    assert isinstance(result["direct_impacts"], dict)

@pytest.mark.asyncio
async def test_cost_analysis_agent_valid():
    agent = CostAnalysisAgent()
    input_data = {
        "materials": ["Bamboo", "Hemp"],
        "quantities": [100, 200],
        "budget": 5000
    }
    result = await agent.process(input_data)
    assert "direct_costs" in result
    assert isinstance(result["direct_costs"], dict)

@pytest.mark.asyncio
async def test_recommendation_agent_valid():
    agent = RecommendationAgent()
    input_data = {
        "materials": ["Bamboo", "Hemp"],
        "quantities": [100, 200],
        "budget": 5000,
        "preferences": {
            "environmental_priority": 0.4,
            "cost_priority": 0.3,
            "recyclability_priority": 0.15,
            "biodegradability_priority": 0.15
        }
    }
    result = await agent.process(input_data)
    assert "recommended_materials" in result
    assert isinstance(result["recommended_materials"], list)

@pytest.mark.asyncio
async def test_material_selection_agent_full_process():
    agent = MaterialSelectionAgent()
    input_data = {
        "materials": ["Bamboo", "Hemp"],
        "quantities": [100, 200],
        "budget": 5000,
        "preferences": {
            "environmental_priority": 0.4,
            "cost_priority": 0.3,
            "recyclability_priority": 0.15,
            "biodegradability_priority": 0.15
        }
    }
    result = await agent.process(input_data)
    assert "environmental_impact" in result
    assert "cost_analysis" in result
    assert "recommendation" in result
    assert "conversation_history" in result
    assert isinstance(result["conversation_history"], list)

# Error handling and edge cases
@pytest.mark.asyncio
async def test_invalid_input_missing_quantities():
    agent = MaterialSelectionAgent()
    input_data = {
        "materials": ["Bamboo", "Hemp"]
        # Missing quantities
    }
    with pytest.raises(Exception):
        await agent.process(input_data)

@pytest.mark.asyncio
async def test_invalid_input_mismatched_lengths():
    agent = MaterialSelectionAgent()
    input_data = {
        "materials": ["Bamboo", "Hemp"],
        "quantities": [100]  # Mismatched lengths
    }
    with pytest.raises(Exception):
        await agent.process(input_data)

@pytest.mark.asyncio
async def test_empty_materials_defaults_to_all():
    agent = MaterialSelectionAgent()
    input_data = {
        # No materials or quantities provided
    }
    result = await agent.process(input_data)
    assert "environmental_impact" in result
    assert "cost_analysis" in result
    assert "recommendation" in result
    assert "conversation_history" in result
    assert isinstance(result["conversation_history"], list) 