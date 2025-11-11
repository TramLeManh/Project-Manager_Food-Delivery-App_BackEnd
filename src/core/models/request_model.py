from dataclasses import dataclass
from typing import List, Any

from fastapi import Query
from pydantic import BaseModel


class PaginatedRequest(BaseModel):
	page: int = Query(default=1, ge=1, description="Current page number (starting from 1)")
	limit: int = Query(default=10, ge=1, le=100, description="Number of items per page (max 100)")


