from fastapi import APIRouter, Depends
from typing import Annotated
from models.query_schemas import SQueryAdd, SQuery, SQueryId
from database.query_repository import QueryRepository


query_router = APIRouter(
    prefix="/queries",
    tags=["Queries"]
)

@query_router.post("")
async def add_query(
    query: Annotated[SQueryAdd, Depends()],
) -> SQueryId:
    query_id = await QueryRepository.add_one(query)
    return {"ok": True, "query_id": query_id}

@query_router.get("")
async def get_query() -> list[SQuery]:
    queries = await QueryRepository.find_all()
    return queries