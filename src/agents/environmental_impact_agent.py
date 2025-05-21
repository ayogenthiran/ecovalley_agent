from typing import Any, Dict, List, Optional
import pandas as pd
from pathlib import Path
from .base_agent import BaseAgent

class EnvironmentalImpactAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Environmental Impact Agent",
            role_description="Expert in environmental impact assessment and sustainability analysis"
        )
        self.materials_df = self._load_materials_database()
    
    def _load_materials_database(self) -> pd.DataFrame:
        """Load the materials database from CSV."""
        try:
            data_path = Path(__file__).parent.parent.parent / "data" / "materials.csv"
            return pd.read_csv(data_path)
        except Exception as e:
            raise Exception(f"Error loading materials database: {str(e)}")
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process material selections and calculate environmental impact.
        
        Args:
            input_data (Dict[str, Any]): Dictionary containing:
                - materials: List of material names
                - quantities: List of quantities in kg
                
        Returns:
            Dict[str, Any]: Environmental impact assessment
        """
        try:
            # Validate input
            if not self._validate_input(input_data):
                raise ValueError("Invalid input data format")
            
            # Calculate direct impacts
            direct_impacts = self._calculate_direct_impacts(
                input_data["materials"],
                input_data["quantities"]
            )
            
            # Get AI assessment
            ai_assessment = await self._get_ai_assessment(direct_impacts)
            
            # Calculate sustainability score
            sustainability_score = self._calculate_sustainability_score(direct_impacts)
            
            # Generate impact summary
            impact_summary = self._generate_impact_summary(
                direct_impacts,
                ai_assessment,
                sustainability_score
            )
            
            return impact_summary
            
        except Exception as e:
            raise Exception(f"Error processing environmental impact: {str(e)}")
    
    def _validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data format and content."""
        required_keys = ["materials", "quantities"]
        if not all(key in input_data for key in required_keys):
            return False
        
        if len(input_data["materials"]) != len(input_data["quantities"]):
            return False
        
        if not all(isinstance(q, (int, float)) and q > 0 for q in input_data["quantities"]):
            return False
        
        return True
    
    def _calculate_direct_impacts(
        self,
        materials: List[str],
        quantities: List[float]
    ) -> Dict[str, float]:
        """Calculate direct environmental impacts for the given materials."""
        total_energy = 0
        total_carbon = 0
        total_water = 0
        total_cost = 0
        
        for material, quantity in zip(materials, quantities):
            material_data = self.materials_df[
                self.materials_df["material_name"] == material
            ].iloc[0]
            
            total_energy += material_data["energy_per_kg"] * quantity
            total_carbon += material_data["carbon_per_kg"] * quantity
            total_water += material_data["water_per_kg"] * quantity
            total_cost += material_data["cost_per_kg"] * quantity
        
        return {
            "total_energy_kwh": round(total_energy, 2),
            "total_carbon_kg": round(total_carbon, 2),
            "total_water_liters": round(total_water, 2),
            "total_cost_usd": round(total_cost, 2)
        }
    
    async def _get_ai_assessment(self, impacts: Dict[str, float]) -> str:
        """Get qualitative assessment from AI model."""
        prompt = f"""
        Analyze these environmental impacts and provide a brief assessment:
        - Energy Usage: {impacts['total_energy_kwh']} kWh
        - Carbon Emissions: {impacts['total_carbon_kg']} kg CO2e
        - Water Usage: {impacts['total_water_liters']} liters
        - Total Cost: ${impacts['total_cost_usd']}
        
        Provide a brief assessment of the environmental impact and suggestions for improvement.
        """
        
        return await self.get_ai_response(prompt, temperature=0.7)
    
    def _calculate_sustainability_score(self, impacts: Dict[str, float]) -> float:
        """Calculate overall sustainability score (0-100)."""
        # Normalize impacts to 0-100 scale (lower is better)
        energy_score = max(0, 100 - (impacts["total_energy_kwh"] * 2))
        carbon_score = max(0, 100 - (impacts["total_carbon_kg"] * 10))
        water_score = max(0, 100 - (impacts["total_water_liters"] * 0.1))
        
        # Weight the scores (can be adjusted based on priorities)
        weights = {
            "energy": 0.3,
            "carbon": 0.4,
            "water": 0.3
        }
        
        sustainability_score = (
            energy_score * weights["energy"] +
            carbon_score * weights["carbon"] +
            water_score * weights["water"]
        )
        
        return round(sustainability_score, 2)
    
    def _generate_impact_summary(
        self,
        impacts: Dict[str, float],
        ai_assessment: str,
        sustainability_score: float
    ) -> Dict[str, Any]:
        """Generate comprehensive impact summary."""
        return {
            "direct_impacts": impacts,
            "ai_assessment": ai_assessment,
            "sustainability_score": sustainability_score,
            "sustainability_level": self._get_sustainability_level(sustainability_score)
        }
    
    def _get_sustainability_level(self, score: float) -> str:
        """Convert numerical score to sustainability level."""
        if score >= 80:
            return "Excellent"
        elif score >= 60:
            return "Good"
        elif score >= 40:
            return "Moderate"
        else:
            return "Needs Improvement" 