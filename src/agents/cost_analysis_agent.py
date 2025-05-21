from typing import Any, Dict, List, Optional
import pandas as pd
from pathlib import Path
from .base_agent import BaseAgent

class CostAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Cost Analysis Agent",
            role_description="Expert in cost analysis, market research, and budget optimization for sustainable materials"
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
        Process material selections and perform cost analysis.
        
        Args:
            input_data (Dict[str, Any]): Dictionary containing:
                - materials: List of material names
                - quantities: List of quantities in kg
                - budget: Optional maximum budget in USD
                
        Returns:
            Dict[str, Any]: Cost analysis results
        """
        try:
            # Validate input
            if not self._validate_input(input_data):
                raise ValueError("Invalid input data format")
            
            # Calculate direct costs
            direct_costs = self._calculate_direct_costs(
                input_data["materials"],
                input_data["quantities"]
            )
            
            # Get market analysis
            market_analysis = await self._get_market_analysis(
                input_data["materials"],
                direct_costs
            )
            
            # Check budget constraints if budget is provided
            budget_check = None
            if "budget" in input_data:
                budget_check = self._check_budget_constraints(
                    direct_costs["total_cost_usd"],
                    input_data["budget"]
                )
            
            # Get optimization suggestions
            optimization_suggestions = await self._get_optimization_suggestions(
                input_data["materials"],
                input_data["quantities"],
                direct_costs,
                budget_check
            )
            
            # Generate cost summary
            cost_summary = self._generate_cost_summary(
                direct_costs,
                market_analysis,
                budget_check,
                optimization_suggestions
            )
            
            return cost_summary
            
        except Exception as e:
            raise Exception(f"Error processing cost analysis: {str(e)}")
    
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
        
        return True
    
    def _calculate_direct_costs(
        self,
        materials: List[str],
        quantities: List[float]
    ) -> Dict[str, float]:
        """Calculate direct costs for the given materials."""
        total_cost = 0
        material_costs = {}
        
        for material, quantity in zip(materials, quantities):
            material_data = self.materials_df[
                self.materials_df["material_name"] == material
            ].iloc[0]
            
            cost = material_data["cost_per_kg"] * quantity
            total_cost += cost
            material_costs[material] = round(cost, 2)
        
        return {
            "total_cost_usd": round(total_cost, 2),
            "material_costs": material_costs,
            "average_cost_per_kg": round(total_cost / sum(quantities), 2)
        }
    
    async def _get_market_analysis(
        self,
        materials: List[str],
        costs: Dict[str, float]
    ) -> str:
        """Get market analysis from AI model."""
        prompt = f"""
        Analyze the current market conditions for these materials and their costs:
        {', '.join(materials)}
        
        Total Cost: ${costs['total_cost_usd']}
        Average Cost per kg: ${costs['average_cost_per_kg']}
        
        Provide a brief market analysis including:
        1. Current market trends
        2. Price competitiveness
        3. Supply chain considerations
        4. Potential cost fluctuations
        """
        
        return await self.get_ai_response(prompt, temperature=0.7)
    
    def _check_budget_constraints(
        self,
        total_cost: float,
        budget: float
    ) -> Dict[str, Any]:
        """Check if the total cost is within budget constraints."""
        is_within_budget = total_cost <= budget
        remaining_budget = max(0, budget - total_cost)
        percentage_used = (total_cost / budget) * 100 if budget > 0 else 0
        
        return {
            "is_within_budget": is_within_budget,
            "remaining_budget": round(remaining_budget, 2),
            "percentage_used": round(percentage_used, 2),
            "budget_exceeded_by": round(max(0, total_cost - budget), 2)
        }
    
    async def _get_optimization_suggestions(
        self,
        materials: List[str],
        quantities: List[float],
        costs: Dict[str, float],
        budget_check: Optional[Dict[str, Any]]
    ) -> str:
        """Get cost optimization suggestions from AI model."""
        prompt = f"""
        Analyze these materials and their costs for optimization opportunities:
        {', '.join(materials)}
        
        Current Costs:
        - Total Cost: ${costs['total_cost_usd']}
        - Average Cost per kg: ${costs['average_cost_per_kg']}
        """
        
        if budget_check:
            prompt += f"""
            Budget Status:
            - Within Budget: {budget_check['is_within_budget']}
            - Remaining Budget: ${budget_check['remaining_budget']}
            - Budget Used: {budget_check['percentage_used']}%
            """
        
        prompt += """
        Provide specific suggestions for:
        1. Cost reduction opportunities
        2. Alternative materials
        3. Quantity optimization
        4. Supply chain improvements
        """
        
        return await self.get_ai_response(prompt, temperature=0.7)
    
    def _generate_cost_summary(
        self,
        costs: Dict[str, float],
        market_analysis: str,
        budget_check: Optional[Dict[str, Any]],
        optimization_suggestions: str
    ) -> Dict[str, Any]:
        """Generate comprehensive cost summary."""
        summary = {
            "direct_costs": costs,
            "market_analysis": market_analysis,
            "optimization_suggestions": optimization_suggestions
        }
        
        if budget_check:
            summary["budget_analysis"] = budget_check
        
        return summary 