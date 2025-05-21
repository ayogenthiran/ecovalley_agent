from typing import Any, Dict, List, Optional, Tuple
import pandas as pd
from pathlib import Path
from .base_agent import BaseAgent
from .environmental_impact_agent import EnvironmentalImpactAgent
from .cost_analysis_agent import CostAnalysisAgent

class RecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Recommendation Agent",
            role_description="Expert in sustainable material selection, combining environmental impact and cost analysis to provide optimal recommendations"
        )
        self.materials_df = self._load_materials_database()
        self.environmental_agent = EnvironmentalImpactAgent()
        self.cost_agent = CostAnalysisAgent()
    
    def _load_materials_database(self) -> pd.DataFrame:
        """Load the materials database from CSV."""
        try:
            data_path = Path(__file__).parent.parent.parent / "data" / "materials.csv"
            return pd.read_csv(data_path)
        except Exception as e:
            raise Exception(f"Error loading materials database: {str(e)}")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process material selections and generate recommendations.
        
        Args:
            input_data (Dict[str, Any]): Dictionary containing:
                - materials: List of material names
                - quantities: List of quantities in kg
                - budget: Optional maximum budget in USD
                - preferences: Optional dictionary of user preferences
                    - environmental_priority: float (0-1)
                    - cost_priority: float (0-1)
                    - recyclability_priority: float (0-1)
                    - biodegradability_priority: float (0-1)
                
        Returns:
            Dict[str, Any]: Recommendation results
        """
        try:
            # Validate input
            if not self._validate_input(input_data):
                raise ValueError("Invalid input data format")
            
            # Get environmental impact analysis
            env_impact = await self.environmental_agent.process(input_data)
            
            # Get cost analysis
            cost_analysis = await self.cost_agent.process(input_data)
            
            # Calculate material scores
            material_scores = self._calculate_material_scores(
                input_data["materials"],
                env_impact,
                cost_analysis,
                input_data.get("preferences", {})
            )
            
            # Generate trade-off analysis
            trade_off_analysis = await self._generate_trade_off_analysis(
                material_scores,
                env_impact,
                cost_analysis
            )
            
            # Get alternative suggestions
            alternatives = await self._get_alternative_suggestions(
                material_scores,
                input_data.get("preferences", {})
            )
            
            # Generate recommendation reasoning
            reasoning = await self._generate_recommendation_reasoning(
                material_scores,
                trade_off_analysis,
                alternatives
            )
            
            # Generate final recommendation
            recommendation = self._generate_recommendation(
                material_scores,
                trade_off_analysis,
                alternatives,
                reasoning
            )
            
            return recommendation
            
        except Exception as e:
            raise Exception(f"Error processing recommendations: {str(e)}")
    
    def _validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data format and content."""
        required_keys = ["materials", "quantities"]
        if not all(key in input_data for key in required_keys):
            return False
        
        if len(input_data["materials"]) != len(input_data["quantities"]):
            return False
        
        if not all(isinstance(q, (int, float)) and q > 0 for q in input_data["quantities"]):
            return False
        
        if "budget" in input_data and not isinstance(input_data["budget"], (int, float)):
            return False
        
        if "preferences" in input_data:
            pref = input_data["preferences"]
            priority_keys = [
                "environmental_priority",
                "cost_priority",
                "recyclability_priority",
                "biodegradability_priority"
            ]
            if not all(key in pref for key in priority_keys):
                return False
            if not all(0 <= pref[key] <= 1 for key in priority_keys):
                return False
        
        return True
    
    def _convert_rating_to_float(self, rating: str) -> float:
        """Convert string ratings to float values."""
        rating_map = {
            "High": 0.9,
            "Medium": 0.6,
            "Low": 0.3,
            "Very High": 1.0,
            "Very Low": 0.1
        }
        return rating_map.get(rating, 0.5)  # Default to 0.5 if rating not found

    def _calculate_material_scores(
        self,
        materials: List[str],
        env_impact: Dict[str, Any],
        cost_analysis: Dict[str, Any],
        preferences: Dict[str, float]
    ) -> Dict[str, float]:
        """Calculate comprehensive scores for each material."""
        scores = {}
        
        # Default priorities if not specified
        priorities = {
            "environmental_priority": 0.4,
            "cost_priority": 0.3,
            "recyclability_priority": 0.15,
            "biodegradability_priority": 0.15
        }
        priorities.update(preferences)
        
        # Normalization constants (domain knowledge or dataset max values)
        MAX_ENERGY = 2000.0  # kWh
        MAX_CARBON = 1000.0  # kg
        MAX_WATER = 100000.0  # liters
        MAX_COST = float(cost_analysis["direct_costs"]["total_cost_usd"]) if float(cost_analysis["direct_costs"]["total_cost_usd"]) > 0 else 1.0
        
        for material in materials:
            material_data = self.materials_df[
                self.materials_df["material_name"] == material
            ].iloc[0]
            
            # Environmental score (0-100, normalized)
            norm_energy = min(float(env_impact["direct_impacts"]["total_energy_kwh"]) / MAX_ENERGY, 1.0)
            norm_carbon = min(float(env_impact["direct_impacts"]["total_carbon_kg"]) / MAX_CARBON, 1.0)
            norm_water = min(float(env_impact["direct_impacts"]["total_water_liters"]) / MAX_WATER, 1.0)
            env_score = 100 - (
                (norm_energy * 0.4 + norm_carbon * 0.4 + norm_water * 0.2) * 100
            )
            
            # Cost score (0-100, normalized)
            material_cost = cost_analysis["direct_costs"].get("material_costs", {}).get(material, 0.0)
            norm_cost = min(float(material_cost) / MAX_COST, 1.0)
            cost_score = 100 - (norm_cost * 100)
            
            # Recyclability score (0-100)
            recyclability_score = self._convert_rating_to_float(material_data["recyclability"]) * 100
            
            # Biodegradability score (0-100)
            biodegradability_score = self._convert_rating_to_float(material_data["biodegradability"]) * 100
            
            # Calculate weighted total score
            total_score = float(
                env_score * priorities["environmental_priority"] +
                cost_score * priorities["cost_priority"] +
                recyclability_score * priorities["recyclability_priority"] +
                biodegradability_score * priorities["biodegradability_priority"]
            )
            
            # Clamp score to 0-100
            scores[material] = round(max(0, min(total_score, 100)), 2)
        
        return scores
    
    async def _generate_trade_off_analysis(
        self,
        material_scores: Dict[str, float],
        env_impact: Dict[str, Any],
        cost_analysis: Dict[str, Any]
    ) -> str:
        """Generate trade-off analysis between materials."""
        prompt = f"""
        Analyze the trade-offs between these materials based on their scores and impacts:
        
        Material Scores:
        {', '.join(f'{m}: {s}' for m, s in material_scores.items())}
        
        Environmental Impact:
        - Energy Usage: {env_impact['direct_impacts']['total_energy_kwh']} kWh
        - Carbon Emissions: {env_impact['direct_impacts']['total_carbon_kg']} kg CO2e
        - Water Usage: {env_impact['direct_impacts']['total_water_liters']} liters
        
        Cost Analysis:
        - Total Cost: ${cost_analysis['direct_costs']['total_cost_usd']}
        - Average Cost per kg: ${cost_analysis['direct_costs']['average_cost_per_kg']}
        
        Provide a detailed trade-off analysis considering:
        1. Environmental impact vs. cost
        2. Performance characteristics
        3. Supply chain considerations
        4. Long-term sustainability
        """
        
        return await self.get_ai_response(prompt, temperature=0.7)
    
    async def _get_alternative_suggestions(
        self,
        material_scores: Dict[str, float],
        preferences: Dict[str, float]
    ) -> str:
        """Get alternative material suggestions."""
        prompt = f"""
        Based on the current material scores and preferences:
        {', '.join(f'{m}: {s}' for m, s in material_scores.items())}
        
        Preferences:
        - Environmental Priority: {preferences.get('environmental_priority', 0.4)}
        - Cost Priority: {preferences.get('cost_priority', 0.3)}
        - Recyclability Priority: {preferences.get('recyclability_priority', 0.15)}
        - Biodegradability Priority: {preferences.get('biodegradability_priority', 0.15)}
        
        Suggest alternative materials that could:
        1. Improve environmental impact
        2. Reduce costs
        3. Enhance recyclability
        4. Increase biodegradability
        
        Consider both direct alternatives and innovative solutions.
        """
        
        return await self.get_ai_response(prompt, temperature=0.7)
    
    async def _generate_recommendation_reasoning(
        self,
        material_scores: Dict[str, float],
        trade_off_analysis: str,
        alternatives: str
    ) -> str:
        """Generate detailed reasoning for the recommendations."""
        prompt = f"""
        Based on the following information, provide detailed reasoning for material recommendations:
        
        Material Scores:
        {', '.join(f'{m}: {s}' for m, s in material_scores.items())}
        
        Trade-off Analysis:
        {trade_off_analysis}
        
        Alternative Suggestions:
        {alternatives}
        
        Provide comprehensive reasoning that:
        1. Explains the scoring methodology
        2. Justifies the recommendations
        3. Addresses potential concerns
        4. Suggests implementation strategies
        """
        
        return await self.get_ai_response(prompt, temperature=0.7)
    
    def _generate_recommendation(
        self,
        material_scores: Dict[str, float],
        trade_off_analysis: str,
        alternatives: str,
        reasoning: str
    ) -> Dict[str, Any]:
        """Generate final recommendation summary."""
        # Sort materials by score
        sorted_materials = sorted(
            material_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "recommended_materials": [
                {
                    "material": material,
                    "score": score,
                    "rank": i + 1
                }
                for i, (material, score) in enumerate(sorted_materials)
            ],
            "trade_off_analysis": trade_off_analysis,
            "alternative_suggestions": alternatives,
            "recommendation_reasoning": reasoning
        } 