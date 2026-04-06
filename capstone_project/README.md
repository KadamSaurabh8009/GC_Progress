**🍽️ Multimodal AI Recipe Assistant**

An AI-powered Multimodal Recipe Recommendation System that suggests recipes based on text queries, filters, and food images using RAG (Retrieval-Augmented Generation), Qdrant Vector Database, and Gemini LLM & Vision models.

**Project Overview**

The Multimodal Recipe Assistant helps users discover recipes by:

Asking natural language queries (e.g. “Quick Indian dinner under 30 minutes”)

Applying smart filters (cuisine, cooking time, vegetarian preference)

Uploading food images to identify dishes and get recipe suggestions

The system uses semantic search + LLM reasoning to generate natural, human-like recipe explanations instead of raw database output.

**Key Features**

1. Natural language recipe search
2. Image-based recipe understanding (Vision AI)
3. Cuisine, cooking time, vegetarian filters
4. Semantic vector search using Qdrant
5. RAG-based response generation
6. Clean Streamlit UI with filters sidebar
7. FastAPI backend with modular architecture
8. Pytest-based unit testing

**🧠 System Architecture**
Streamlit (Frontend)
        |
FastAPI (Backend API)
        |
Query Se;rvice (RAG Orchestrator)
        |
Retriever (Qdrant Vector Search)
        |
Gemini LLM + Gemini Vision

**Tech Stack**
Frontend: Streamlit

Backend:FastAPI and Python 3.11+

AI / ML
Sentence Transformers (MiniLM)
Gemini LLM (Text Generation)
Gemini Vision (Image Understanding)

Vector Database
Qdrant

Testing
Pytest


**Installation & Setup**
 Step 1: Clone Repository
git clone https://github.com/<username>/multimodal-recipe-bot.git
cd capstone_project

 Step 2: Create Virtual Environment
python -m venv new_venv
new_venv\Scripts\activate   # Windows

 Step 3: Install Dependencies
pip install -r requirements.txt

 Step 4: Start Qdrant
docker run -p 6333:6333 qdrant/qdrant

 Step 5: Ingest Recipe Data
python -m scripts.store_qdrant

 Step 6: Run Backend (FastAPI)
uvicorn app.main:app --reload

 Step 7: Run Frontend (Streamlit)
cd frontend
streamlit run streamlit_app.py

**API Endpoints**
🔹 Health Check
GET /health

🔹 Recipe Query
POST /query


Request Body

{
  "query": "Quick Indian dinner",
  "cuisine": "Indian",
  "max_time": 30,
  "veg_only": true
}


Response

{
  "answer": "Here are some quick and delicious Indian dinner ideas..."
}

🔹 Vision-Based Query
POST /vision


Upload food image

Returns dish description and suggestions
