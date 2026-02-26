from fastapi import APIRouter, Depends, HTTPException

from schemas.query import QueryRequest, QueryResponse
from api.dependencies import get_rag_engine
from services.rag_engine import RAGEngine

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    rag_engine: RAGEngine = Depends(get_rag_engine)
):
    try:
        print("____________________________________________")
        print("Получили запрос и отправряем его в цепочку RAG")
        answer = rag_engine.query(request.question)
        print("____________________________________________")
        print("Получили ответ, возвращаем его обратно")
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))