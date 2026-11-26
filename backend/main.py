from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import importlib
import pkgutil
import backend.routes as routes

app = FastAPI()

# allow React to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # this needs to match the frontend
    allow_methods=["*"],
    allow_headers=["*"],
)

# dynamically import all modules in routes folder
for loader, module_name, is_pkg in pkgutil.iter_modules(routes.__path__):
    module = importlib.import_module(f"backend.routes.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)


@app.post("/api/compute")
def compute(data: dict):
    x = data["value"]
    return {"result": x * x}
