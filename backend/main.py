from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import pandas as pd
from .utils import filter_branches_within_radius
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from sqlalchemy import create_engine

# Specify the SQLite database file name
sqlite_db_file = "subway.db"

# Create a SQLite engine
engine = create_engine(f"sqlite:///{sqlite_db_file}")


# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_branches")
async def get_branches():
    df = pd.read_sql("subway_table", engine)

    names = df["name"].unique().tolist()
    return {"names": names}


@app.post("/get_data")
async def get_data(selected_station: str):
    df = pd.read_sql("subway_table", engine)
    df.drop(
        columns=["operating_hours", "address", "google_maps_link", "waze_link"],
        inplace=True,
    )

    # Filter data based on the selected station
    selected_station_data = df[df["name"] == selected_station]
    branch_location = (
        selected_station_data["latitude"].astype(float).values[0],
        selected_station_data["longitude"].astype(float).values[0],
    )

    # Get all branches within 5 km
    branches_within_radius = filter_branches_within_radius(
        branch_location, df, selected_station
    )

    return {
        "branch_location": branch_location,
        "selected_station": selected_station,
        "branches_within_radius": branches_within_radius,
    }


@app.post("/response")
async def response(query: str):
    llm = ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="gpt-4-0125-preview",
    )

    df = pd.read_sql("subway_table", engine)
    df.drop(
        columns=["google_maps_link", "waze_link", "latitude", "longitude"], inplace=True
    )
    table_info = df.to_string()
    prompt_template = """The following are all the data of Subway branches in Kuala Lumpur Malaysia:
    {table_info}

    You have to answer user's question from the above details.

    You have to go through all the data to find the answer.

    Your response must be very kind, do not mentioned data in your response.

    User's Question: {question}"""
    prompt = PromptTemplate(
        input_variables=["table_info", "question"], template=prompt_template
    )
    llm = LLMChain(
        llm=llm,
        prompt=prompt,
    )
    result = llm.invoke({"table_info": table_info, "question": query})
    return {"response": result["text"]}
