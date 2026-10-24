from fastapi import FastAPI

from .routes import asset_types, assets, relationship_types, relationships

app = FastAPI()
app.include_router(asset_types.router)
app.include_router(assets.router)
app.include_router(relationship_types.router)
app.include_router(relationships.router)
