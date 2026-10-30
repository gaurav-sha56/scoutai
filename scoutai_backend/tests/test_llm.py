import os
import sys
import pytest
from dotenv import load_dotenv
from crewai import LLM

# Load environment variables from .env file
load_dotenv()


@pytest.mark.parametrize("model_name", [
    "groq/openai/gpt-oss-120b",
    "groq/openai/gpt-oss-20b",
])
def test_llm_working(model_name: str):
    """
    Test 1: Test the API key and whether the LLM class is properly working.

    Parameter:
        model_name (str): The name/path of the model (e.g. 'groq/openai/gpt-oss-120b')
    """
    # 1. Verify that the required API key for the model provider exists
    if model_name.startswith("groq/"):
        groq_key = os.getenv("GROQ_API_KEY")
        assert groq_key, (
            f"GROQ_API_KEY environment variable is missing for model '{model_name}'. "
            "Please create a .env file (copy from .env.example) and set your GROQ_API_KEY."
        )
    elif model_name.startswith("openai/"):
        assert os.getenv("OPENAI_API_KEY"), "OPENAI_API_KEY environment variable is missing."
    elif model_name.startswith("anthropic/"):
        assert os.getenv("ANTHROPIC_API_KEY"), "ANTHROPIC_API_KEY environment variable is missing."

    # 2. Create the LLM instance
    llm = LLM(model=model_name)
    assert llm is not None, f"Failed to instantiate LLM with model: {model_name}"
    assert llm.model == model_name, f"Expected LLM model to be '{model_name}', got '{llm.model}'"

    # 3. Test the LLM with a lightweight test call
    response = llm.call("Respond with just 'OK'")
    assert response is not None, f"LLM call returned None for model: {model_name}"

    response_text = str(response).strip()
    assert len(response_text) > 0, f"LLM call returned empty response for model: {model_name}"
    print(f"\n[PASS] Model '{model_name}' successfully tested. Response: {response_text[:40]}")


if __name__ == "__main__":
    # Support running this test directly as a script:
    # python tests/test_llm.py [model_name]
    target_model = sys.argv[1] if len(sys.argv) > 1 else "groq/openai/gpt-oss-120b"
    print(f"Running LLM API test with model: {target_model}")
    test_llm_working(target_model)
    print("Test passed successfully!")
