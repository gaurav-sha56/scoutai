#!/usr/bin/env python
import warnings
from scoutai_backend.crew import ScoutaiBackend
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")




# query class
class Query(BaseModel):
    startup : str = Field(description="Name of the startup")
    domain : str = Field(description="domain of the startup")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000","https://scoutai-lilac.vercel.app/"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# uncomment this if you want to run through the crewai-cli
# def run():
#     """
#     Run the crew.
#     """
#     domain = <your startup domain>
#     startup =  < your startup name >
#
#     inputs = {
#         'domain': domain,
#         'our_startup' : startup
#     }


#     try:
#         result = ScoutaiBackend().crew().kickoff(inputs=inputs)
#         print(result.raw)
#     except Exception as e:
#         raise Exception(f"An error occurred while running the crew: {e}")

@app.post('/run_crew')
async def run_async(query : Query):
    inputs = {
        'domain' : query.domain,
        'our_startup' : query.startup
    }
    try:
        crew_response = result = ScoutaiBackend().crew().kickoff(inputs=inputs)
        return {
            "status" : "ok",
            "report_md" : crew_response.raw
        }
    except Exception as e:
        if "rate_limit" in str(e).lower() or "RateLimitError" in str(e):
            raise HTTPException(status_code=429, detail="Rate limit hit, try again in 30s")
        raise HTTPException(status_code=500, detail=str(e))