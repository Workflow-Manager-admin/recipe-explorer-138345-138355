from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..schemas import BookmarkCreate, BookmarkRead
from ..models import Bookmark, Recipe
from ..deps import get_db, get_current_user

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/", summary="Bookmark a recipe", response_model=BookmarkRead)
def bookmark_recipe(
    data: BookmarkCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Save a recipe to user's favorites/bookmarks"""
    recipe = db.query(Recipe).filter(Recipe.id == data.recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    already = db.query(Bookmark).filter(
        Bookmark.user_id == user.id, Bookmark.recipe_id == data.recipe_id
    ).first()
    if already:
        raise HTTPException(status_code=400, detail="Already bookmarked")
    new_bm = Bookmark(user_id=user.id, recipe_id=data.recipe_id)
    db.add(new_bm)
    db.commit()
    db.refresh(new_bm)
    return new_bm

# PUBLIC_INTERFACE
@router.delete("/{recipe_id}", summary="Remove bookmark by recipe_id")
def remove_bookmark(recipe_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Remove a recipe from user's saved/bookmarked recipes."""
    bm = db.query(Bookmark).filter_by(user_id=user.id, recipe_id=recipe_id).first()
    if not bm:
        raise HTTPException(status_code=404, detail="Not bookmarked")
    db.delete(bm)
    db.commit()
    return {"ok": True}

# PUBLIC_INTERFACE
@router.get("/", summary="List my bookmarked recipes", response_model=List[BookmarkRead])
def list_bookmarks(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """List all recipes bookmarked by the current user."""
    return db.query(Bookmark).filter_by(user_id=user.id).all()
