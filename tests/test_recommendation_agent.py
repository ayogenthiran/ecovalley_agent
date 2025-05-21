import pytest
import pandas as pd
from pathlib import Path
from src.agents.recommendation_agent import RecommendationAgent

@pytest.fixture
def sample_materials_data():
    """Create a sample materials database for testing."""
    data = {
        "material_name": ["Bamboo", "Hemp", "Recycled PET"],
        "energy_per_kg": [2.5, 3.0, 4.0],
        "carbon_per_kg": [1.2, 1.5, 2.0],
        "water_per_kg": [100, 120, 80],
        "cost_per_kg": [5.0, 4.5, 3.0],
        "recyclability": [0.8, 0.7, 0.9],
        "biodegradability": [0.9, 0.8, 0.3]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_input_data():
    """Create sample input data for testing."""
    return {
        "materials": ["Bamboo", "Hemp", "Recycled PET"],
        "quantities": [100, 150, 200],
        "budget": 5000,
        "preferences": {
            "environmental_priority": 0.4,
            "cost_priority": 0.3,
            "recyclability_priority": 0.15,
            "biodegradability_priority": 0.15
        }
    }

@pytest.fixture
def mock_environmental_impact(mocker):
    """Mock environmental impact analysis results."""
    return {
        "direct_impacts": {
            "total_energy_kwh": 1000,
            "total_carbon_kg": 500,
            "total_water_liters": 50000
        }
    }

@pytest.fixture
def mock_cost_analysis(mocker):
    """Mock cost analysis results."""
    return {
        "direct_costs": {
            "total_cost_usd": 4000,
            "average_cost_per_kg": 8.89,
            "material_costs": {
                "Bamboo": 500,
                "Hemp": 675,
                "Recycled PET": 600
            }
        }
    }

@pytest.mark.asyncio
async def test_agent_initialization():
    """Test that the agent initializes correctly."""
    agent = RecommendationAgent()
    assert agent.name == "Recommendation Agent"
    assert isinstance(agent.materials_df, pd.DataFrame)
    assert not agent.materials_df.empty

@pytest.mark.asyncio
async def test_input_validation(sample_input_data):
    """Test input validation with valid and invalid data."""
    agent = RecommendationAgent()
    
    # Test valid input
    assert agent._validate_input(sample_input_data) is True
    
    # Test invalid input - missing required key
    invalid_input = sample_input_data.copy()
    del invalid_input["materials"]
    assert agent._validate_input(invalid_input) is False
    
    # Test invalid input - mismatched lengths
    invalid_input = sample_input_data.copy()
    invalid_input["quantities"] = [100, 150]  # One less than materials
    assert agent._validate_input(invalid_input) is False
    
    # Test invalid input - negative quantity
    invalid_input = sample_input_data.copy()
    invalid_input["quantities"] = [100, -150, 200]
    assert agent._validate_input(invalid_input) is False

@pytest.mark.asyncio
async def test_material_score_calculation(
    sample_input_data,
    mock_environmental_impact,
    mock_cost_analysis
):
    """Test material score calculation."""
    agent = RecommendationAgent()
    
    scores = agent._calculate_material_scores(
        sample_input_data["materials"],
        mock_environmental_impact,
        mock_cost_analysis,
        sample_input_data["preferences"]
    )
    
    # Check that scores are calculated for all materials
    assert len(scores) == len(sample_input_data["materials"])
    
    # Check that scores are within expected range (0-100)
    assert all(0 <= score <= 100 for score in scores.values())
    
    # Check that scores are properly rounded
    assert all(isinstance(score, float) for score in scores.values())
    assert all(score == round(score, 2) for score in scores.values())

@pytest.mark.asyncio
async def test_trade_off_analysis(
    sample_input_data,
    mock_environmental_impact,
    mock_cost_analysis
):
    """Test trade-off analysis generation."""
    agent = RecommendationAgent()
    
    # Calculate scores first
    scores = agent._calculate_material_scores(
        sample_input_data["materials"],
        mock_environmental_impact,
        mock_cost_analysis,
        sample_input_data["preferences"]
    )
    
    # Generate trade-off analysis
    analysis = await agent._generate_trade_off_analysis(
        scores,
        mock_environmental_impact,
        mock_cost_analysis
    )
    
    # Check that analysis is a non-empty string
    assert isinstance(analysis, str)
    assert len(analysis) > 0

@pytest.mark.asyncio
async def test_alternative_suggestions(sample_input_data):
    """Test alternative suggestions generation."""
    agent = RecommendationAgent()
    
    # Create sample scores
    scores = {
        "Bamboo": 85.5,
        "Hemp": 78.2,
        "Recycled PET": 82.1
    }
    
    # Generate alternatives
    alternatives = await agent._get_alternative_suggestions(
        scores,
        sample_input_data["preferences"]
    )
    
    # Check that alternatives is a non-empty string
    assert isinstance(alternatives, str)
    assert len(alternatives) > 0

@pytest.mark.asyncio
async def test_recommendation_reasoning(
    sample_input_data,
    mock_environmental_impact,
    mock_cost_analysis
):
    """Test recommendation reasoning generation."""
    agent = RecommendationAgent()
    
    # Calculate scores
    scores = agent._calculate_material_scores(
        sample_input_data["materials"],
        mock_environmental_impact,
        mock_cost_analysis,
        sample_input_data["preferences"]
    )
    
    # Generate trade-off analysis
    trade_off = await agent._generate_trade_off_analysis(
        scores,
        mock_environmental_impact,
        mock_cost_analysis
    )
    
    # Generate alternatives
    alternatives = await agent._get_alternative_suggestions(
        scores,
        sample_input_data["preferences"]
    )
    
    # Generate reasoning
    reasoning = await agent._generate_recommendation_reasoning(
        scores,
        trade_off,
        alternatives
    )
    
    # Check that reasoning is a non-empty string
    assert isinstance(reasoning, str)
    assert len(reasoning) > 0

@pytest.mark.asyncio
async def test_full_recommendation_process(sample_input_data):
    """Test the complete recommendation process."""
    agent = RecommendationAgent()
    
    # Process the recommendation
    recommendation = await agent.process(sample_input_data)
    
    # Check the structure of the recommendation
    assert isinstance(recommendation, dict)
    assert "recommended_materials" in recommendation
    assert "trade_off_analysis" in recommendation
    assert "alternative_suggestions" in recommendation
    assert "recommendation_reasoning" in recommendation
    
    # Check recommended materials structure
    materials = recommendation["recommended_materials"]
    assert isinstance(materials, list)
    assert len(materials) == len(sample_input_data["materials"])
    
    # Check each material entry
    for material in materials:
        assert "material" in material
        assert "score" in material
        assert "rank" in material
        assert isinstance(material["score"], float)
        assert isinstance(material["rank"], int)
        assert 0 <= material["score"] <= 100 