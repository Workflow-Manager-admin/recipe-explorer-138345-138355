from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, Table, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

# Association tables
recipe_ingredients = Table(
    "recipe_ingredients", Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id"), primary_key=True),
)

recipe_tags = Table(
    "recipe_tags", Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    recipes = relationship("Recipe", back_populates="owner", cascade="all, delete")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete")


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text)
    steps = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner = relationship("User", back_populates="recipes")
    ingredients = relationship("Ingredient", secondary=recipe_ingredients, back_populates="recipes")
    tags = relationship("Tag", secondary=recipe_tags, back_populates="recipes")
    bookmarks = relationship("Bookmark", back_populates="recipe", cascade="all, delete")


class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    recipes = relationship("Recipe", secondary=recipe_ingredients, back_populates="ingredients")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    recipes = relationship("Recipe", secondary=recipe_tags, back_populates="tags")


class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="bookmarks")
    recipe = relationship("Recipe", back_populates="bookmarks")
