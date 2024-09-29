from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException # type: ignore
from langchain_google_genai import GoogleGenerativeAI # type: ignore
from langchain_core.prompts import PromptTemplate # type: ignore
from pydantic import BaseModel
import os

app = FastAPI()

load_dotenv()

# Define a dynamic prompt template for the automotive assistant
prompt_template = """
Your custom prompt here.
Define variables and behavior for your assistant.

input: {your_data}
"""

# Initialize the prompt template with dynamic variables
code_assistant_template = PromptTemplate(
    input_variables=["your variables"],
    template=prompt_template
)

# Define Pydantic model for the request body
class AutoRequest(BaseModel):
    your_data: str

@app.post("/autogenerate")
async def autogenerate(request: AutoRequest):
    # Validate the presence of Google API key in the environment variable
    if not os.environ.get("GOOGLE_API_KEY"):
        raise HTTPException(status_code=500, detail="Google API key not found. Please set the environment variable GOOGLE_API_KEY.")

    # Initialize the GoogleGenerativeAI model with sensible defaults and error handling
    try:
        llm = GoogleGenerativeAI(model="gemini-pro", temperature=0.2, google_api_key=os.environ["GOOGLE_API_KEY"])
    except Exception as e:
        print(f"Error initializing GoogleGenerativeAI: {e}")
        raise HTTPException(status_code=500, detail="Failed to initialize AI model.")

    # Prepare the inputs for the prompt
    prompt_inputs = {
        "input": request.your_data,
    }

    # Chain the prompt template and model
    llm_chain = code_assistant_template | llm

    # Invoke the chain with the dynamic inputs and handle potential errors
    try:
        # Removed the await keyword since invoke is likely not async
        response = llm_chain.invoke(prompt_inputs)
    except Exception as e:
        print(f"Error generating code: {e}")
        raise HTTPException(status_code=500, detail="Failed to get response.")

    return {"response": response}
