from fastapi import FastAPI
from routes.auth_routes import router as auth_routes
from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.models import OAuthFlows
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import RedirectResponse
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Your API Title",
        version="1.0.0",
        description="Your API Description",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    openapi_schema["components"]["security"] = [
        {"BearerAuth": []}
    ]
    for path in openapi_schema["paths"].values():
        for methods in path.values():
            if isinstance(methods, dict):
                methods["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url="/docs/oauth2-redirect",
        init_oauth={
            "clientId": "your-client-id",
            "clientSecret": None,
            "scopeSeparator": " ",
            "scopes": {},
        },
    )

@app.get("/docs/oauth2-redirect")
async def oauth2_redirect():
    return RedirectResponse(url="/docs")

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_json():
    return app.openapi()

app.include_router(router=auth_routes, prefix="/auth", tags=["auth"])