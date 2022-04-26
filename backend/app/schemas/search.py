from typing import Literal, Optional, Dict, List

from pydantic import BaseModel


class SearchSchema(BaseModel):
    filter: Optional[Dict[str, list]]
    fields: Optional[List[str]]
    limit: Optional[int] = 100
    page: Optional[int] = 1
    sort: Optional[Dict[str, Literal["asc", "desc"]]]
