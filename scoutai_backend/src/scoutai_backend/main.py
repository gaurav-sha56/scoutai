#!/usr/bin/env python
import warnings
from scoutai_backend.crew import ScoutaiBackend
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from functools import partial
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")




# query class
class Query(BaseModel):
    startup : str = Field(description="Name of the startup")
    domain : str = Field(description="domain of the startup")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Run the crew function
def run(domain: str = "artificial intelligence", startup_name: str = "ScoutAI"):
    """
    Run the crew with domain and startup name.

    Args:
        domain (str): Domain of the startup (defaults to 'artificial intelligence')
        startup_name (str): Name of the startup (defaults to 'ScoutAI')
    """
    inputs = {
        'domain': domain,
        'our_startup': startup_name
    }

    try:
        result = ScoutaiBackend().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def test(domain: str = "artificial intelligence", startup_name: str = "ScoutAI"):
    """
    Test function to test the run function with domain and startup name parameters.

    Args:
        domain (str): Domain of the startup (e.g., 'artificial intelligence')
        startup_name (str): Name of the startup (e.g., 'ScoutAI')
    """
    print(f"Testing run function with domain='{domain}' and startup_name='{startup_name}'...")
    result = run(domain=domain, startup_name=startup_name)
    print("Crew run completed successfully.")
    return result


def train():
    """Train the crew for a given number of iterations."""
    raise NotImplementedError("Training is not configured yet.")


def replay():
    """Replay the crew execution from a specific task."""
    raise NotImplementedError("Replay is not configured yet.")


def run_with_trigger():
    """Run the crew with external trigger."""
    return run()

@app.post('/run_crew')
async def run_async(query: Query):
    inputs = {
        'domain': query.domain,
        'our_startup': query.startup
    }
    try:
        loop = asyncio.get_event_loop()
        crew_response = await loop.run_in_executor(
            None, 
            partial(ScoutaiBackend().crew().kickoff, inputs=inputs)
        )
        return {"status": "ok", "report_md": crew_response.raw}
    except Exception as e:
        print(e)
        if "rate_limit" in str(e).lower():
            raise HTTPException(status_code=429, detail="Rate limit hit, try again in 30s")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import sys
    domain_arg = sys.argv[1] if len(sys.argv) > 1 else "artificial intelligence"
    startup_arg = sys.argv[2] if len(sys.argv) > 2 else "ScoutAI"
    test(domain=domain_arg, startup_name=startup_arg)
