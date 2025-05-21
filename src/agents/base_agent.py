from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from openai import AsyncOpenAI
from ..config.settings import get_settings

class BaseAgent(ABC):
    def __init__(self, name: str, role_description: str):
        """
        Initialize the base agent.
        
        Args:
            name (str): Name of the agent
            role_description (str): Description of the agent's role and capabilities
        """
        self.name = name
        self.role_description = role_description
        self.settings = get_settings()
        self.client = AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)
    
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the input data and return results.
        Must be implemented by concrete agent classes.
        
        Args:
            input_data (Dict[str, Any]): Input data to process
            
        Returns:
            Dict[str, Any]: Processed results
        """
        pass
    
    async def get_ai_response(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> str:
        """
        Get a response from the OpenAI API.
        
        Args:
            prompt (str): The prompt to send to the AI
            temperature (float, optional): Controls randomness. Defaults to 0.7
            max_tokens (int, optional): Maximum tokens in response. Defaults to 1000
            
        Returns:
            str: AI response text
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": self.role_description},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error getting AI response: {str(e)}")
    
    def __str__(self) -> str:
        """String representation of the agent."""
        return f"{self.name} - {self.role_description}" 