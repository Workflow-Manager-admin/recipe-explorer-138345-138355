from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, users, recipes, bookmarks
from .db import Base, engine

# App metadata for OpenAPI/docs
app = FastAPI(
    title="Recipe Explorer Backend",
    description="Backend API for fullstack recipe app: authentication, user management, recipes, search, bookmarks.",
    version="1.0.0",
    openapi_tags=[
        {"name": "auth", "description": "User registration/login"},
        {"name": "user", "description": "User profile and account"},
        {"name": "recipes", "description": "Recipe management and search"},
        {"name": "bookmarks", "description": "Bookmark/favorite recipes"},
    ]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    # Create tables if necessary (for development/demo; use Alembic in prod)
    Base.metadata.create_all(bind=engine)

# Health check
@app.get("/", tags=["health"])
def health_check():
    """Ping the backend to check if it is up."""
    return {"message": "Healthy"}

# API Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["user"])
app.include_router(recipes.router, prefix="/recipes", tags=["recipes"])
app.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])
