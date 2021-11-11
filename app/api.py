from collections import defaultdict
from typing import Dict, List

import spacy
import srsly
import uvicorn
from fastapi import Body, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.models import ENT_PROP_MAP, RecordsEntitiesByTypeResponse, RecordsRequest, RecordsResponse
from app.spacy_extractor import SpacyExtractor

app = FastAPI(
    title="NER API",
    version="1.0",
    description="Microservice of NER using spaCy and FastAPI",
)

example_request = srsly.read_json("app/data/example_request.json")

nlp = spacy.load("xx_ent_wiki_sm")
extractor = SpacyExtractor(nlp)


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse("docs")


@app.post("/api/entities", response_model=RecordsResponse, tags=["NER"])
async def extract_entities(body: RecordsRequest = Body(..., example=example_request)):
    """Extract Named Entities from a batch of Records."""

    documents: List[Dict] = []

    for val in body.values:
        documents.append({"id": val.recordId, "text": val.data.text})

    entities_res = extractor.extract_entities(documents)

    res = [{"recordId": er["id"], "data": {"entities": er["entities"]}} for er in entities_res]

    return {"values": res}


@app.post("/api/entities_by_type", response_model=RecordsEntitiesByTypeResponse, tags=["NER"])
async def extract_entities_by_type(body: RecordsRequest = Body(..., example=example_request)):
    """Extract Named Entities from a batch of Records separated by entity label."""

    documents: List[Dict] = []

    for val in body.values:
        documents.append({"id": val.recordId, "text": val.data.text})

    entities_res = extractor.extract_entities(documents)
    res: List[Dict] = []

    for er in entities_res:
        groupby = defaultdict(list)
        for ent in er["entities"]:
            ent_prop = ENT_PROP_MAP[ent["label"]]
            groupby[ent_prop].append(ent["name"])
        record = {"recordId": er["id"], "data": groupby}
        res.append(record)

    return {"values": res}
