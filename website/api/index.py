from typing import Union
from fastapi import FastAPI, Query, HTTPException, HTMLResponse, Depends
import requests

def thaiToUnicode(text):
    unicode_text = ''.join([f'\\u{ord(char):04x}' for char in text])
    return unicode_text


url = 'https://raw.githubusercontent.com/ronnapatp/ParliamentTracker/main/data/representatives.json'

response = requests.get(url)
fileContent = response.json()

app = FastAPI()

@app.get("/api/representatives")
def read_root(ID: Union[str, None] = Query(None, description="Representative ID filter"),
               Party: Union[str, None] = Query(None, description="Representative party filter (Thai)")):
    if ID:
        filteredMemberID = [member for member in fileContent if member.get("ID") == ID]
        if not filteredMemberID:
            raise HTTPException(status_code=404, detail="Member not found")
        return filteredMemberID
    elif Party:
        print(f"Searching for party: {Party}")
        unicodePartyName = thaiToUnicode(Party)  
        print(unicodePartyName)
        filteredMemberParty = [member for member in fileContent if
                               thaiToUnicode(member.get("Party", "")).strip() == unicodePartyName]
        print(f"Found {len(filteredMemberParty)} members.")
        if not filteredMemberParty:
            raise HTTPException(status_code=404, detail="Members not found")
        return filteredMemberParty
    return fileContent
