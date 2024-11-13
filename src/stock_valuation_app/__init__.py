from fastapi import FastAPI
from .api.routes import router
from .ui.dashboard import app as dash_app

app = FastAPI()
app.include_router(router)

# Mount Dash app
app.mount("/dashboard", dash_app.server)
