from typing import Any, Dict, List, Optional
from .base_agent import BaseAgent
from .recommendation_agent import RecommendationAgent
from .environmental_impact_agent import EnvironmentalImpactAgent
from .cost_analysis_agent import CostAnalysisAgent

class MaterialSelectionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Material Selection Agent",
            role_description="Coordinator agent that manages the material selection workflow, delegates to specialized agents, and maintains conversation context."
        )
        self.recommendation_agent = RecommendationAgent()
        self.environmental_agent = EnvironmentalImpactAgent()
        self.cost_agent = CostAnalysisAgent()
        self.conversation_history: List[Dict[str, Any]] = []

    def add_to_history(self, user_input: Dict[str, Any], agent_outputs: Dict[str, Any]):
        self.conversation_history.append({
            "user_input": user_input,
            "agent_outputs": agent_outputs
        })

    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrate the material selection workflow:
        1. Analyze user request
        2. Get candidate materials
        3. Delegate to specialized agents
        4. Compile and return the final response
        """
        # Step 1: Analyze user request (could be extended for NLP, etc.)
        user_request = input_data

        # Step 2: Get candidate materials (for now, use provided or all in DB)
        # If user specifies materials, use them; otherwise, use all available
        if "materials" not in user_request or not user_request["materials"]:
            user_request["materials"] = list(self.recommendation_agent.materials_df["material_name"].values)
            user_request["quantities"] = [1 for _ in user_request["materials"]]  # Default quantity

        # Step 3: Delegate to specialized agents
        # Environmental impact
        env_impact = await self.environmental_agent.process(user_request)
        # Cost analysis
        cost_analysis = await self.cost_agent.process(user_request)
        # Recommendation
        recommendation = await self.recommendation_agent.process(user_request)

        # Step 4: Compile the final response
        final_response = {
            "environmental_impact": env_impact,
            "cost_analysis": cost_analysis,
            "recommendation": recommendation,
            "conversation_history": self.conversation_history
        }

        # Maintain conversation context
        self.add_to_history(user_request, final_response)

        return final_response 