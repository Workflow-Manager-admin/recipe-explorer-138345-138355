from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..schemas import RecipeCreate, RecipeUpdate, RecipeRead
from ..models import Recipe, Ingredient, Tag
from ..deps import get_db, get_current_user
from sqlalchemy import or_

router = APIRouter()

# PUBLIC_INTERFACE
@router.get("/", response_model=List[RecipeRead], summary="List/search recipes")
def list_recipes(
    q: Optional[str] = Query(None, description="Search in title/desc/ingredient/tag"),
    tag: Optional[str] = Query(None, description="Filter by tag name"),
    ingredient: Optional[str] = Query(None, description="Filter by ingredient name"),
    db: Session = Depends(get_db),
    skip: int = 0, limit: int = 20
):
    """
    List/search/filter recipes.
    """
    qry = db.query(Recipe).distinct()
    if q:
        qry = qry.filter(or_(
            Recipe.title.ilike(f"%{q}%"),
            Recipe.description.ilike(f"%{q}%"),
            Recipe.steps.ilike(f"%{q}%"),
            Recipe.ingredients.any(Ingredient.name.ilike(f"%{q}%")),
            Recipe.tags.any(Tag.name.ilike(f"%{q}%")),
        ))
    if tag:
        qry = qry.filter(Recipe.tags.any(Tag.name == tag))
    if ingredient:
        qry = qry.filter(Recipe.ingredients.any(Ingredient.name == ingredient))
    return qry.offset(skip).limit(limit).all()

# PUBLIC_INTERFACE
@router.post("/", response_model=RecipeRead, summary="Create a recipe")
def create_recipe(
    data: RecipeCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Create new recipe for current user."""
    recipe = Recipe(
        title=data.title,
        description=data.description,
        steps=data.steps,
        owner_id=user.id,
    )
    # Ingredients
    if data.ingredient_names:
        for iname in data.ingredient_names:
            ing = db.query(Ingredient).filter(Ingredient.name == iname).first()
            if not ing:
                ing = Ingredient(name=iname)
                db.add(ing)
            recipe.ingredients.append(ing)
    # Tags
    if data.tag_names:
        for tname in data.tag_names:
            tag = db.query(Tag).filter(Tag.name == tname).first()
            if not tag:
                tag = Tag(name=tname)
                db.add(tag)
            recipe.tags.append(tag)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

# PUBLIC_INTERFACE
@router.get("/{recipe_id}", response_model=RecipeRead, summary="Get recipe details")
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """View recipe by ID."""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe

# PUBLIC_INTERFACE
@router.put("/{recipe_id}", response_model=RecipeRead, summary="Update (your) recipe")
def update_recipe(
    recipe_id: int,
    data: RecipeUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """Update a recipe. Only owner can update."""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    recipe.title = data.title
    recipe.description = data.description
    recipe.steps = data.steps
    # Update ingredients
    if data.ingredient_names is not None:
        recipe.ingredients.clear()
        for iname in data.ingredient_names:
            ing = db.query(Ingredient).filter(Ingredient.name == iname).first()
            if not ing:
                ing = Ingredient(name=iname)
                db.add(ing)
            recipe.ingredients.append(ing)
    # Update tags
    if data.tag_names is not None:
        recipe.tags.clear()
        for tname in data.tag_names:
            tag = db.query(Tag).filter(Tag.name == tname).first()
            if not tag:
                tag = Tag(name=tname)
                db.add(tag)
            recipe.tags.append(tag)
    db.commit()
    db.refresh(recipe)
    return recipe

# PUBLIC_INTERFACE
@router.delete("/{recipe_id}", summary="Delete (your) recipe")
def delete_recipe(recipe_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Delete a recipe; only owner may delete."""
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    if recipe.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    db.delete(recipe)
    db.commit()
    return {"ok": True}
