from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from src.agents.material_selection_agent import MaterialSelectionAgent
import numpy as np

router = APIRouter()

class MaterialRequest(BaseModel):
    materials: Optional[List[str]] = Field(None, description="List of candidate material names")
    quantities: Optional[List[float]] = Field(None, description="Quantities for each material (kg)")
    budget: Optional[float] = Field(None, description="Maximum budget in USD")
    preferences: Optional[Dict[str, float]] = Field(None, description="User preference weights (0-1) for environmental, cost, recyclability, biodegradability")

class MaterialResponse(BaseModel):
    environmental_impact: Dict[str, Any]
    cost_analysis: Dict[str, Any]
    recommendation: Dict[str, Any]
    conversation_history: List[Dict[str, Any]]

def convert_numpy_types(obj):
    if isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    return obj

material_agent = MaterialSelectionAgent()

@router.post("/materials/suggest", response_model=MaterialResponse)
async def suggest_materials(request: MaterialRequest):
    try:
        # Prepare input data for the agent
        input_data = request.dict(exclude_unset=True)
        # If quantities are provided, ensure they match materials
        if input_data.get("materials") and input_data.get("quantities"):
            if len(input_data["materials"]) != len(input_data["quantities"]):
                raise HTTPException(status_code=400, detail="Length of materials and quantities must match.")
        # Call the agent
        result = await material_agent.process(input_data)
        # Convert numpy types to Python native types
        converted_result = convert_numpy_types(result)
        return MaterialResponse(**converted_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 