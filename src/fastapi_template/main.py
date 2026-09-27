from fastapi import FastAPI

from fastapi_template.domains import router as domain_routers

app = FastAPI(
    title="FastAPI Project Template",
    description="Template for FastAPI applications.",
    version="1.0.0",
)

app.include_router(
    domain_routers,
)
