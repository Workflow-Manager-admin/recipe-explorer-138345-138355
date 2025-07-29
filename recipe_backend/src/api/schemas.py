from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# -- USER SCHEMAS --

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = ""

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserRead(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    class Config:
        orm_mode = True

# -- INGREDIENT SCHEMA --

class IngredientBase(BaseModel):
    name: str

class IngredientRead(IngredientBase):
    id: int
    class Config:
        orm_mode = True

# -- TAG SCHEMA --

class TagBase(BaseModel):
    name: str

class TagRead(TagBase):
    id: int
    class Config:
        orm_mode = True

# -- RECIPE SCHEMAS --

class RecipeBase(BaseModel):
    title: str
    description: Optional[str] = ""
    steps: Optional[str] = ""
    ingredient_names: Optional[List[str]] = []
    tag_names: Optional[List[str]] = []

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(RecipeBase):
    pass

class RecipeRead(RecipeBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    ingredients: List[IngredientRead]
    tags: List[TagRead]
    class Config:
        orm_mode = True

# -- BOOKMARKS --

class BookmarkCreate(BaseModel):
    recipe_id: int

class BookmarkRead(BaseModel):
    id: int
    recipe: RecipeRead
    created_at: datetime
    class Config:
        orm_mode = True

# -- JWT Token Schemas --

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None
