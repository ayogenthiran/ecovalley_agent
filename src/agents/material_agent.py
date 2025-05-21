from typing import Any, Dict, List
from .base_agent import BaseAgent
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class MaterialSuggestion(BaseModel):
    materials: List[str] = Field(description="List of suggested materials")
    reasoning: str = Field(description="Reasoning behind the material selection")

class MaterialSelectionAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert in sustainable material selection. Your task is to suggest appropriate materials based on the given requirements."),
            ("user", "{input}")
        ])
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Format the prompt
        formatted_prompt = self.prompt.format_messages(
            input=f"Product Type: {input_data['product_type']}\nRequirements: {input_data['requirements']}"
        )
        
        # Get response from LLM
        response = await self.llm.ainvoke(formatted_prompt)
        
        # For now, return a simple response
        return {
            "materials": ["Material 1", "Material 2"],
            "reasoning": response.content
        }
    
    async def validate(self, input_data: Dict[str, Any]) -> bool:
        required_fields = ["product_type", "requirements"]
        return all(field in input_data for field in required_fields) 