
import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL_NAME = "openai/gpt-oss-120b"


# ==========================================
# GROQ CLIENT
# ==========================================
def get_client():
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY missing in .env file")

    return Groq(api_key=api_key)


# ==========================================
# GENERAL AI FUNCTION
# ==========================================
def ask_ai(prompt, max_tokens=2500):

    client = get_client()

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert software architect and AI developer. "
                    "Give clear, structured, practical answers. "
                    "Avoid unnecessary repetition."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content or ""


# ==========================================
# 1. SYSTEM DESIGN
# ==========================================
def generate_system_design(project_idea):

    prompt = f"""
Create a system design for this project:

{project_idea[:1500]}

Use these sections:

1. Project Overview
2. Functional Requirements
3. Non-Functional Requirements
4. System Architecture
5. Main Components
6. Data Flow
7. Recommended Technologies
8. Scalability
9. Conclusion

Keep the explanation useful, clear and concise.
"""

    return ask_ai(prompt, max_tokens=2000)


# ==========================================
# 2. FEATURE ANALYSIS
# ==========================================
def generate_feature_analysis(project_idea, feature):

    prompts = {
        "Tech Stack Recommendation": """
Recommend an appropriate technology stack.

Include:
- Frontend
- Backend
- Programming language
- Database
- AI/ML technology if needed
- APIs
- Deployment

Explain why each technology is suitable.
""",

        "Database Design": """
Design a database for the project.

Include:
- Table names
- Columns and data types
- Primary keys
- Foreign keys
- Relationships
- Short explanation of each table

Use a readable format.
""",

        "Security Analysis": """
Perform a security analysis for this project.

Include:
- Important security risks
- Authentication and authorization
- Data protection
- API security
- Input validation
- Prevention methods
- Security recommendations

Use practical and understandable points.
""",

        "Architecture Diagram": """
Describe the architecture components and their connections.

Return a simple structured explanation of:
- User
- Frontend
- Backend
- Services
- Database
- External APIs

Do not generate a diagram here. The diagram tool handles visualization.
""",

        "PDF Report": """
Prepare a concise system design report summary.

Include project overview, system architecture, technologies,
database summary, security summary and conclusion.
"""
    }

    feature_prompt = prompts.get(feature, feature)

    prompt = f"""
Project: {project_idea[:1200]}

Task: {feature}

Instructions:
{feature_prompt}

Give a structured answer using headings and bullet points.
Avoid unnecessary content.
"""

    return ask_ai(prompt, max_tokens=2000)


# ==========================================
# 3. ARCHITECTURE COMPONENTS (JSON)
# ==========================================
def generate_architecture_components(project_idea):

    prompt = f"""
Create a simple architecture diagram structure for:

{project_idea[:1000]}

Return ONLY valid JSON. No markdown.

Format:
{{
  "nodes": [
    {{"id": "A", "label": "User"}},
    {{"id": "B", "label": "Frontend"}}
  ],
  "edges": [
    {{"from": "A", "to": "B"}}
  ]
}}

Use 5 to 9 nodes.
Keep node IDs short.
"""

    try:
        result = ask_ai(prompt, max_tokens=1200)

        result = result.strip()

        if result.startswith("```"):
            result = result.replace("```json", "")
            result = result.replace("```", "")
            result = result.strip()

        data = json.loads(result)

        if "nodes" in data and "edges" in data:
            return data

        return None

    except Exception as e:
        print("Architecture JSON Error:", e)
        return None


# ==========================================
# 4. AI CODE GENERATION - TOKEN OPTIMIZED
# ==========================================
def generate_project_code(project_idea, system_design):

    # System design text intentionally shortened
    if isinstance(system_design, str):
        short_design = system_design[:2500]
    else:
        short_design = str(system_design)[:2500]

    short_idea = str(project_idea)[:1200]

    prompt = f"""
Build a beginner-friendly working project based on this idea.

PROJECT IDEA:
{short_idea}

SYSTEM DESIGN SUMMARY:
{short_design}

REQUIREMENTS:
1. Use a simple and suitable technology stack.
2. Give the folder structure.
3. Generate working code for the main files.
4. Keep code simple and readable.
5. Include requirements.txt.
6. Include .env.example if API keys are required.
7. Include installation instructions.
8. Include run instructions.
9. Avoid unnecessary files and long explanations.
10. Do not use placeholder code such as "implement this later".

OUTPUT FORMAT:

# Project Title

## Folder Structure

## Installation

## requirements.txt

## Main Source Code
Give complete code for each important file in separate code blocks.

## How to Run

## Future Improvements

Generate a compact but functional implementation.
"""

    # Lower output limit to reduce TPM consumption
    return ask_ai(prompt, max_tokens=2500)


# ==========================================
# 5. CONNECTION TEST
# ==========================================
def test_ai_connection():

    try:
        answer = ask_ai(
            "Reply with: ArchitecAI AI connection successful.",
            max_tokens=100
        )

        return answer

    except Exception as e:
        return f"Connection failed: {e}"
