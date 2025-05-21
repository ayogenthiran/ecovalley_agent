import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))  # project root
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))  # src
sys.path.append(str(Path(__file__).resolve().parent.parent / "config"))  # config

import asyncio
from src.agents.cost_analysis_agent import CostAnalysisAgent

async def main():
    # Create agent instance
    agent = CostAnalysisAgent()
    
    # Print agent info
    print(f"Agent Name: {agent.name}")
    print(f"Role Description: {agent.role_description}")
    
    # Print materials database info
    print("\nMaterials Database:")
    print(f"Number of materials: {len(agent.materials_df)}")
    print("\nAvailable materials:")
    for material in agent.materials_df["material_name"]:
        print(f"- {material}")
    
    # Test cost calculation
    test_data = {
        "materials": ["Bamboo", "Recycled PET"],
        "quantities": [10.0, 5.0],
        "budget": 1000.0
    }
    
    print("\nCalculating costs...")
    result = await agent.process(test_data)
    
    print("\nResults:")
    print("\nDirect Costs:")
    print(f"Total Cost: ${result['direct_costs']['total_cost_usd']}")
    print(f"Average Cost per kg: ${result['direct_costs']['average_cost_per_kg']}")
    print("\nMaterial Costs:")
    for material, cost in result['direct_costs']['material_costs'].items():
        print(f"- {material}: ${cost}")
    
    print("\nBudget Analysis:")
    budget = result['budget_analysis']
    print(f"Within Budget: {budget['is_within_budget']}")
    print(f"Remaining Budget: ${budget['remaining_budget']}")
    print(f"Budget Used: {budget['percentage_used']}%")
    if not budget['is_within_budget']:
        print(f"Budget Exceeded by: ${budget['budget_exceeded_by']}")
    
    print("\nMarket Analysis:")
    print(result['market_analysis'])
    
    print("\nOptimization Suggestions:")
    print(result['optimization_suggestions'])

if __name__ == "__main__":
    asyncio.run(main()) 