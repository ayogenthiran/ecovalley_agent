import pytest
import pandas as pd
from src.agents.cost_analysis_agent import CostAnalysisAgent

@pytest.fixture
def agent():
    """Create an instance of CostAnalysisAgent for testing."""
    return CostAnalysisAgent()

def test_agent_initialization(agent):
    """Test that the agent initializes correctly."""
    assert agent.name == "Cost Analysis Agent"
    assert isinstance(agent.materials_df, pd.DataFrame)
    assert not agent.materials_df.empty

def test_materials_database_columns(agent):
    """Test that the materials database has the expected columns."""
    expected_columns = [
        "material_name",
        "energy_per_kg",
        "carbon_per_kg",
        "water_per_kg",
        "cost_per_kg",
        "recyclability",
        "biodegradability"
    ]
    assert all(col in agent.materials_df.columns for col in expected_columns)

def test_direct_cost_calculation(agent):
    """Test direct cost calculation for a single material."""
    # Test with Bamboo
    materials = ["Bamboo"]
    quantities = [10.0]  # 10 kg
    
    costs = agent._calculate_direct_costs(materials, quantities)
    
    assert "total_cost_usd" in costs
    assert "material_costs" in costs
    assert "average_cost_per_kg" in costs
    assert "Bamboo" in costs["material_costs"]
    assert costs["total_cost_usd"] == costs["material_costs"]["Bamboo"]
    assert costs["average_cost_per_kg"] == costs["total_cost_usd"] / 10.0

def test_budget_constraints(agent):
    """Test budget constraint checking."""
    # Test within budget
    budget_check = agent._check_budget_constraints(500.0, 1000.0)
    assert budget_check["is_within_budget"] is True
    assert budget_check["remaining_budget"] == 500.0
    assert budget_check["percentage_used"] == 50.0
    assert budget_check["budget_exceeded_by"] == 0.0
    
    # Test exceeding budget
    budget_check = agent._check_budget_constraints(1500.0, 1000.0)
    assert budget_check["is_within_budget"] is False
    assert budget_check["remaining_budget"] == 0.0
    assert budget_check["percentage_used"] == 150.0
    assert budget_check["budget_exceeded_by"] == 500.0

@pytest.mark.asyncio
async def test_full_cost_analysis(agent):
    """Test complete cost analysis process."""
    test_data = {
        "materials": ["Bamboo", "Recycled PET"],
        "quantities": [10.0, 5.0],
        "budget": 1000.0
    }
    
    result = await agent.process(test_data)
    
    # Check result structure
    assert "direct_costs" in result
    assert "market_analysis" in result
    assert "optimization_suggestions" in result
    assert "budget_analysis" in result
    
    # Check direct costs
    costs = result["direct_costs"]
    assert "total_cost_usd" in costs
    assert "material_costs" in costs
    assert "average_cost_per_kg" in costs
    assert "Bamboo" in costs["material_costs"]
    assert "Recycled PET" in costs["material_costs"]
    
    # Check budget analysis
    budget = result["budget_analysis"]
    assert "is_within_budget" in budget
    assert "remaining_budget" in budget
    assert "percentage_used" in budget
    assert "budget_exceeded_by" in budget 