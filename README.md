# Loss Detection - Senior Design Project

## Overview

The Loss Detection project aims to develop a scalable machine-learning solution to identify potentially stolen items from Craigslist listings. This project assists loss prevention professionals by providing a data-driven tool that leverages both classical machine learning and a large language model (LLM) to enhance data analysis and decision-making.

## Problem Statement

Retailers face significant losses when shoplifters resell stolen goods online, and manual searching through over 40 million Craigslist listings is impractical. Our solution seeks to automatically analyze these listings to:
- Determine the likelihood of a listing being linked to stolen items.
- Provide a user-friendly dashboard with actionable insights for retail partners.

## Objectives and Scope

- **Objectives:**
  - Develop a machine learning classifier to predict if a listing is stolen.
  - Integrate a large language model (LLM) for advanced prompt engineering and data analysis.
  - Create an interactive dashboard that displays analysis by location and category.
  - **[Additional objectives to be added]**

- **Scope:**
  - Focus on specific categories (e.g., over-the-counter drugs, apparel).
  - Tailor results for diverse retail needs.
  - **[Further scope details to be defined]**

## Technology Stack [WIP]

- **Programming Language:** Python
- **Machine Learning:** scikit-learn, TensorFlow, or PyTorch (for classifier development)
- **LLM Integration:**  
  - Local deployment and/or API key usage for integrating an LLM  
  - Techniques in prompt engineering to refine model outputs
- **Data Processing:** Pandas, NumPy
- **Dashboard:** PowerBI for creating interactive visualizations and reporting
- **Deployment:** GitHub Pages for hosting project documentation

## LLM Integration

Our project will integrate an LLM to support advanced analysis through prompt engineering. The LLM can be deployed locally or accessed via an API key. This component will be used to:
- Enhance classification accuracy by refining input prompts.
- Assist with natural language processing tasks within the data pipeline.
- **[Further details and usage instructions to be added]**

## Installation Instructions [WIP]

1. **Prerequisites:**
   - Python 3.x
   - Git

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/loss-detection-senior-design.git
   cd loss-detection-senior-design

3. **Set Up the Python Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   pip install -r requirements.txt
4. **Configuration**
  - Create a .env file for environment variables (e.g. API keys)
  ```bash
   LLM_API_KEY=your_api_key_here
   DATABASE_URL=your_database_url_here
   ```
5. **Running the Application**
  ```bash
   python app.py
   ```
## Usage Examples
- Interacting with the LLM:
  ```bash
   from llm_module import LLMClient

   llm = LLMClient(api_key="your_api_key_here") 

   prompt = "Analyze the following listing details: [Insert listing data here]"
   response = llm.generate(prompt)
   print(response)
  ```

## Roadmap and Milestones
- Milestone 1: First Sponsor Meeting - 1/22/2025
- Milestone 2: Team Charter - 2/4/2025
- Milestone 3: Initial Data Collection Complete - N/A
- Milestone 4: Wireframe Draft Presentation - 3/5/2025
- Milestone 5: Midterm Presentation - 3/11/2025
- Milestone 6: Code Review - 3/19/2025
- Milestone 7: Dashboard Review - 4/2/2025
- Milestone 8: Last Sponsor Meeting - 4/16/2025
- Milestone 9: Final Presentation - TBD
- Milestone 10: Final Poster - 4/22/2025

## Team and Stakeholders
- Team Name: Loss Detection
- Team Members:
  - Abigail Friedin
  - Stacy Chiok
  - Andrea Riquezes Gete
  - Gage Mowry
  - Devon Yee
  - Kayla Williams
- Faculty Advisor: Alexander Semenov
- Sponsor: Sam Yeung
