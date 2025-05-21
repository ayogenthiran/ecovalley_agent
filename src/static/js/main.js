document.addEventListener('DOMContentLoaded', () => {
    // Update range input values
    const rangeInputs = document.querySelectorAll('input[type="range"]');
    rangeInputs.forEach(input => {
        const valueDisplay = input.nextElementSibling;
        input.addEventListener('input', () => {
            valueDisplay.textContent = input.value;
        });
    });

    // Form submission
    const form = document.getElementById('materialForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state
        document.querySelector('.loading').style.display = 'block';
        document.querySelector('.results-content').style.display = 'none';

        // Prepare form data
        const materials = document.getElementById('materials').value.split(',').map(m => m.trim());
        const quantities = document.getElementById('quantities').value.split(',').map(q => parseFloat(q.trim()));
        const budget = parseFloat(document.getElementById('budget').value);

        const preferences = {
            environmental_priority: parseFloat(document.getElementById('envPriority').value),
            cost_priority: parseFloat(document.getElementById('costPriority').value),
            recyclability_priority: parseFloat(document.getElementById('recyclePriority').value),
            biodegradability_priority: parseFloat(document.getElementById('bioPriority').value)
        };

        try {
            const response = await fetch('/api/v1/materials/suggest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    materials,
                    quantities,
                    budget,
                    preferences
                })
            });

            if (!response.ok) {
                throw new Error('API request failed');
            }

            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while fetching recommendations. Please try again.');
        } finally {
            document.querySelector('.loading').style.display = 'none';
        }
    });
});

function displayResults(data) {
    const resultsContent = document.querySelector('.results-content');
    resultsContent.style.display = 'block';

    // Display recommended materials
    const recommendedMaterials = document.getElementById('recommendedMaterials');
    recommendedMaterials.innerHTML = data.recommendation.recommended_materials
        .map(material => `
            <div class="material-card">
                <h4>${material.material}</h4>
                <p>Score: ${material.score.toFixed(2)}</p>
                <p>Rank: ${material.rank}</p>
            </div>
        `).join('');

    // Display environmental impact
    const environmentalImpact = document.getElementById('environmentalImpact');
    const impacts = data.environmental_impact.direct_impacts;
    environmentalImpact.innerHTML = `
        <p>Total Energy: ${impacts.total_energy_kwh.toFixed(2)} kWh</p>
        <p>Total Carbon: ${impacts.total_carbon_kg.toFixed(2)} kg CO2e</p>
        <p>Total Water: ${impacts.total_water_liters.toFixed(2)} liters</p>
    `;

    // Display cost analysis
    const costAnalysis = document.getElementById('costAnalysis');
    const costs = data.cost_analysis.direct_costs;
    costAnalysis.innerHTML = `
        <p>Total Cost: $${costs.total_cost_usd.toFixed(2)}</p>
        <p>Average Cost per kg: $${costs.average_cost_per_kg.toFixed(2)}</p>
    `;

    // Display trade-off analysis
    const tradeOffAnalysis = document.getElementById('tradeOffAnalysis');
    tradeOffAnalysis.innerHTML = `
        <p>${data.recommendation.trade_off_analysis}</p>
    `;
} 