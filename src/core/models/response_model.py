from dataclasses import dataclass
from typing import List, Any


@dataclass
class PaginatedResult:
	total: int
	page: int
	page_size: int
	data: List[Any]