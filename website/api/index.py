from typing import Union
from fastapi import FastAPI, Query, HTTPException
import requests

app = FastAPI(docs_url="/api", redoc_url=None, openapi_url="/api/openapi.json")


def thaiToUnicode(text):
    unicode_text = ''.join([f'\\u{ord(char):04x}' for char in text])
    return unicode_text


representativesUrl = 'https://raw.githubusercontent.com/ronnapatp/ParliamentTracker/main/data/representatives.json'
representativesResponse = requests.get(representativesUrl)
representativesContent = representativesResponse.json()

@app.get("/api/representatives")
def read_root(ID: Union[str, None] = Query(None, description="Representative ID filter"),
               Party: Union[str, None] = Query(None, description="Representative party filter (Thai)")):
    if ID:
        filteredMemberID = [member for member in representativesContent if member.get("ID") == ID]
        if not filteredMemberID:
            raise HTTPException(status_code=404, detail="Member not found")
        return filteredMemberID
    elif Party:
        print(f"Searching for party: {Party}")
        unicodePartyName = thaiToUnicode(Party)  
        print(unicodePartyName)
        filteredMemberParty = [member for member in representativesContent if
                               thaiToUnicode(member.get("Party", "")).strip() == unicodePartyName]
        print(f"Found {len(filteredMemberParty)} members.")
        if not filteredMemberParty:
            raise HTTPException(status_code=404, detail="Members not found")
        return filteredMemberParty
    return representativesContent

billsUrl = 'https://raw.githubusercontent.com/ronnapatp/ParliamentTracker/main/data/bills.json'
billsResponse = requests.get(billsUrl)
billsContent = billsResponse.json()

@app.get("/api/bills")
def read_root():
    return billsContent