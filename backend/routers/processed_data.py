from fastapi import APIRouter

router = APIRouter(tags=["processed_data"])


@router.get("/processed_data")
def processed_data() -> dict:
    # TODO: Return normalized data generated from uploaded links.
    return {
        "message": "processed_data endpoint scaffolded",
        "data": [],
    }
