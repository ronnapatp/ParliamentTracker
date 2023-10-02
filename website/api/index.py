from typing import Union
from fastapi import FastAPI, Query, HTTPException
import requests


tagsMetadata = [
    {
        "name": "Members",
        "description": "Member of The Parliament of Thailand (Representatives and Senators)",
    },
    {
        "name": "Bills",
        "description": "Bills status in Thailand's parliament",
    },
]

app = FastAPI(
    docs_url="/api",
    redoc_url=None,
    openapi_url="/api/openapi.json",
    title="Parliament Tracker API",
    summary="All APIs about Thailand's Parliament",
    version="0.0.1",
    swagger_ui_parameters={
        "syntaxHighlight.theme":"obsidian"
    },
)

def thaiToUnicode(text):
    unicode_text = ''.join([f'\\u{ord(char):04x}' for char in text])
    return unicode_text



representativesUrl = 'https://raw.githubusercontent.com/ronnapatp/ParliamentTracker/main/data/representatives.json'
representativesResponse = requests.get(representativesUrl)
representativesContent = representativesResponse.json()

@app.get("/api/representatives", tags=["Members"], name="Return a list of lower house members")
def read_root():
    return representativesContent

@app.get("/api/representatives/{id}", tags=["Members"], name="Return member by ID")
async def read_item(id: str):
    item = next((item for item in representativesContent if item["id"] == id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


billsUrl = 'https://raw.githubusercontent.com/ronnapatp/ParliamentTracker/main/data/bills.json'
billsResponse = requests.get(billsUrl)
billsContent = billsResponse.json()

@app.get("/api/bills", tags=["Bills"])
def read_root():
    return billsContent