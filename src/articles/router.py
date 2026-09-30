from typing import Optional, List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorCollection

from src.articles.model import Article
from src.core.dependencies import get_collection

router = APIRouter()


@router.get("/", response_model=List[Article])
async def list_articles(collection: AsyncIOMotorCollection = Depends(get_collection("article"))):
    cursor = collection.find({}, {"_id": 0})
    docs = await cursor.to_list(length=None)
    return [Article(**d) for d in docs]

@router.get("/{article_id}", response_model=Article)
async def get_article(article_id: str, collection: AsyncIOMotorCollection = Depends(get_collection("article"))):
    doc = await collection.find_one({"id": article_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return Article(**doc)
