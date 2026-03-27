from fastapi import APIRouter

router = APIRouter(tags=["upload_link"])


@router.post("/upload_link")
def upload_link(payload: dict) -> dict:
    # TODO: Validate Instagram URL and enqueue processing workflow.
    return {
        "message": "upload_link endpoint scaffolded",
        "received": payload,
    }
