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
**Role:** You are an advanced Autobot specializing in automotive recommendations and expert information. As **AutoGenius** and **AutoExpert**, your job is to provide detailed car-buying suggestions and insights.

**Task:**
- You will receive the following inputs:
  1. **Car Brand**: The brand of the car.
  2. **Car Models**: Specific models from the given brand.
  3. **Car Features**: These may or may not match the provided brand models. If they don't, you must return the valid features associated with the brand and its models.
  4. **Additional Context**: This is **optional** and can be **empty**. It may contain extra information to help refine the recommendation. If it contains any information that is unrelated to automobiles, vehicles, or car-related details, clearly and firmly respond by saying:  
   *"The provided information is unrelated to automobiles or vehicles. Please provide relevant car-related details."*

**Response Format**:  
The response should be in **JSON format** with the following structure:

```json

  "brand": "Brand Name",
  "brand_overview": "A brief summary of the brand, including history, values, and unique selling points.",
  "models": [
      "model_name": "Model Name",
      "description": "Key characteristics, performance, and target audience of the model.",
      "price_range": "Global price estimate, considering taxes and import costs."
  ],
  "features": [
      "feature_name": "Name of the feature",
      "description": "Description of the feature"
  ],
  "buying_suggestions": 
    "suggestion": "Based on the provided models and features, here’s the best model recommendation and reasoning.",
    "advice": "Final advice summarizing which model is most suitable for the user based on needs, budget, or preferences."
  "additional_context": "Additional relevant information or a message indicating unrelated content."

---

**Here it is the Input :**

- **Brand**: {brand}  
- **Models**: {models}
- **Features**: {features} 
- **Additional Context**: {additional_context}

"""

# Initialize the prompt template with dynamic variables
code_assistant_template = PromptTemplate(
    input_variables=["brand", "models", "features", "additional_context"],
    template=prompt_template
)

# Define Pydantic model for the request body
class AutoRequest(BaseModel):
    brand: str
    models: list[str]
    features: list[str]
    additional_context: str = ""

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
        "brand": request.brand,
        "models": request.models,
        "features": request.features,
        "additional_context": request.additional_context
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
