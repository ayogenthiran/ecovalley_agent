# EcoValley Agent System

EcoValley is an agent-based web application for sustainable material selection. It leverages advanced AI agents to analyze environmental impact, cost, and other sustainability factors to recommend optimal materials for your projects.

---

## Features
- **Agent-based architecture**: Modular agents for environmental impact, cost analysis, recommendations, and workflow coordination.
- **Retrieval-Augmented Generation (RAG)**: Integrates structured data and AI reasoning.
- **OpenAI GPT-4o-mini integration**: For advanced reasoning and natural language explanations.
- **RESTful API**: Easily integrate with other systems or frontends.
- **Extensible**: Add new agents or data sources as needed.

---

## Project Structure
```
ecovalley/
├── src/
│   ├── agents/
│   │   ├── base_agent.py
│   │   ├── environmental_impact_agent.py
│   │   ├── cost_analysis_agent.py
│   │   ├── recommendation_agent.py
│   │   └── material_selection_agent.py
│   ├── api/
│   │   └── endpoints/
│   │       └── material.py
│   ├── config/
│   │   └── settings.py
│   ├── main.py
│   └── ...
├── data/
│   └── materials.csv
├── tests/
│   └── test_agents.py
├── .env
├── requirements.txt
└── README.md
```

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ecovalley.git
   cd ecovalley
   ```

2. **Set up a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Create a `.env` file in the project root:
     ```env
     OPENAI_API_KEY=your_openai_api_key_here
     DATABASE_URL=sqlite:///./ecovalley.db
     ```

---

## Running the Application

Start the FastAPI server:
```bash
python src/main.py
```

The API will be available at [http://localhost:8000](http://localhost:8000)

---

## API Documentation

Interactive API docs are available at:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Main Endpoint
#### `POST /api/v1/materials/suggest`
Suggests sustainable materials based on your requirements.

**Request Body Example:**
```json
{
  "materials": ["Bamboo", "Hemp"],
  "quantities": [100, 200],
  "budget": 5000,
  "preferences": {
    "environmental_priority": 0.4,
    "cost_priority": 0.3,
    "recyclability_priority": 0.15,
    "biodegradability_priority": 0.15
  }
}
```

**Response Example:**
```json
{
  "environmental_impact": { ... },
  "cost_analysis": { ... },
  "recommendation": { ... },
  "conversation_history": [ ... ]
}
```

---

## Testing

Run the test suite with:
```bash
pytest tests/test_agents.py -v
```

---

## Customization & Extensibility
- **Add new agents**: Implement new agent classes in `src/agents/` and integrate them in `material_selection_agent.py`.
- **Update materials database**: Edit `data/materials.csv` to add or modify material properties.
- **Change model or API keys**: Update `.env` and `src/config/settings.py` as needed.

---

## Troubleshooting
- Ensure your `.env` file is present and contains a valid OpenAI API key.
- If you encounter import errors, make sure you are running commands from the project root and that your virtual environment is activated.
- For SSL/OpenAI issues, ensure your Python and dependencies are up to date.

---

## License
MIT License

---

## Contact
For questions or contributions, please open an issue or pull request on GitHub.
