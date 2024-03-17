from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routes.home_routes import homeRoutes
from routes.message_routes import messageRoutes
from routes.thread_routes import threadRoutes
from routes.agent_routes import agentRoutes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this in production!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(homeRoutes, prefix="/home", tags=["home"])
app.include_router(messageRoutes, prefix="/message", tags=["message"])
app.include_router(threadRoutes, prefix="/thread", tags=["thread"])
app.include_router(agentRoutes, prefix="/agent", tags=["agent"])
