from fastapi import APIRouter

router = APIRouter(tags=["rag_itinerary"])


@router.post("/rag_itinerary")
def rag_itinerary(payload: dict) -> dict:
    # TODO: Use RAG pipeline to produce itinerary recommendations.
    return {
        "message": "rag_itinerary endpoint scaffolded",
        "request": payload,
    }
