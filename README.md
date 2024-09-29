# AutoAccelerate-API
A Generative AI API Built with Python and FastAPI

## Overview
AutoAccelerate-API is built using **FastAPI** and **Langchain** for handling prompt requests, leveraging top large language models (LLMs) to generate responses. The API architecture allows for dynamic and flexible interaction with LLMs, making it easy to populate prompts and fetch responses based on your specific needs.

### Key Features:
- **Langchain Integration**: Utilizes Langchain for efficient prompt management and interaction with LLMs.
- **FastAPI**: Provides a high-performance, easy-to-use web framework for API endpoints.
- **Modular Design**: Easily customizable prompts and variables for different use cases.

### Packages Used:
- **FastAPI**
- **Langchain**
- **Langchain_Google_Genai**
- **Uvicorn** (for running the FastAPI app)

---

## Setup Guide

### Step 1: Clone the Repository
```bash
git clone <repo_url>
```

### Step 2: Create and Activate Virtual Environment
To set up your Python virtual environment, run the following commands:

```bash
# Create a virtual environment
python -m venv yourenvname

# Activate the environment (Windows)
yourenvname\scripts\Activate

# Activate the environment (MacOS/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies
Install the required packages by running:

```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
Create a `.env` file in the root directory and add the following environment variables:

```bash
GOOGLE_API_KEY=<your_google_api_key> # Obtain this from AIstudio.google.com
LANGCHAIN_TRACING_V2=<your_langchain_tracing_key>
LANGCHAIN_ENDPOINT=<your_langchain_endpoint>
LANGCHAIN_API_KEY=<your_langchain_api_key>
LANGCHAIN_PROJECT=<your_langchain_project>
```

### Step 5: Modify Prompts
Customize the prompt templates in `main.py` to fit your use case.

### Step 6: Run the API
Start the FastAPI server using **Uvicorn**:

```bash
uvicorn main:app
```

### Step 7: Access API Documentation
After starting the server, open your browser and navigate to:

```
http://127.0.0.1:8000/docs
```

This will open the interactive FastAPI documentation where you can test the API endpoints directly.

---

Now you can start using the AutoAccelerate-API to interact with your custom LLM prompts!
