import pytest
import pandas as pd
from src.agents.environmental_impact_agent import EnvironmentalImpactAgent

@pytest.fixture
def agent():
    """Create an instance of EnvironmentalImpactAgent for testing."""
    return EnvironmentalImpactAgent()

def test_agent_initialization(agent):
    """Test that the agent initializes correctly."""
    assert agent.name == "Environmental Impact Agent"
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

def test_materials_database_content(agent):
    """Test that the materials database contains expected materials."""
    expected_materials = [
        "Bamboo",
        "Hemp",
        "Recycled PET",
        "PLA (Polylactic Acid)",
        "Cork",
        "Recycled Aluminum",
        "Recycled Paper",
        "Mushroom Mycelium",
        "Recycled Glass",
        "Organic Cotton"
    ]
    assert all(material in agent.materials_df["material_name"].values 
              for material in expected_materials)

@pytest.mark.asyncio
async def test_impact_calculation(agent):
    """Test environmental impact calculation."""
    test_data = {
        "materials": ["Bamboo", "Recycled PET"],
        "quantities": [10.0, 5.0]
    }
    
    result = await agent.process(test_data)
    
    assert "direct_impacts" in result
    assert "ai_assessment" in result
    assert "sustainability_score" in result
    assert "sustainability_level" in result
    
    impacts = result["direct_impacts"]
    assert "total_energy_kwh" in impacts
    assert "total_carbon_kg" in impacts
    assert "total_water_liters" in impacts
    assert "total_cost_usd" in impacts

def test_sustainability_levels(agent):
    """Test sustainability level categorization."""
    assert agent._get_sustainability_level(85) == "Excellent"
    assert agent._get_sustainability_level(70) == "Good"
    assert agent._get_sustainability_level(50) == "Moderate"
    assert agent._get_sustainability_level(30) == "Needs Improvement" 