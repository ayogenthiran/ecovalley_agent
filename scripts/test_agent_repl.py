import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))  # project root
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))  # src
sys.path.append(str(Path(__file__).resolve().parent.parent / "config"))  # config

import asyncio
from src.agents.environmental_impact_agent import EnvironmentalImpactAgent

async def main():
    # Create agent instance
    agent = EnvironmentalImpactAgent()
    
    # Print agent info
    print(f"Agent Name: {agent.name}")
    print(f"Role Description: {agent.role_description}")
    
    # Print materials database info
    print("\nMaterials Database:")
    print(f"Number of materials: {len(agent.materials_df)}")
    print("\nAvailable materials:")
    for material in agent.materials_df["material_name"]:
        print(f"- {material}")
    
    # Test impact calculation
    test_data = {
        "materials": ["Bamboo", "Recycled PET"],
        "quantities": [10.0, 5.0]
    }
    
    print("\nCalculating environmental impact...")
    result = await agent.process(test_data)
    
    print("\nResults:")
    print(f"Direct Impacts: {result['direct_impacts']}")
    print(f"Sustainability Score: {result['sustainability_score']}")
    print(f"Sustainability Level: {result['sustainability_level']}")
    print(f"\nAI Assessment:\n{result['ai_assessment']}")

if __name__ == "__main__":
    asyncio.run(main()) 