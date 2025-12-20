from fastapi import APIRouter, Depends
from typing import Annotated
from backend.models.user_schemas import SQueryAdd, SQuery
from repository import QueryRepository


query_router = APIRouter(
    prefix="/queries"
)

@query_router.post("")
async def add_query(
    query: Annotated[SQueryAdd, Depends()],
):
    query_id = await QueryRepository.add_one(query)
    return {"ok": True, "query_id": query_id}

@query_router.get("")
async def get_query() -> list[SQuery]:
    queries = await QueryRepository.find_all()
    return queries