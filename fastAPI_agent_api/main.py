from fastapi import FastAPI

from routes.home_routes import homeRoutes

app = FastAPI()

app.include_router(homeRoutes, prefix="/home", tags=["home"])
