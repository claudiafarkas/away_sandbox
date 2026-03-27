from pydantic import BaseModel, HttpUrl


class LinkRecord(BaseModel):
    # TODO: Extend with id, timestamps, and processing metadata.
    source_url: HttpUrl
    source_type: str = "instagram"
