import uvicorn
from fastapi import FastAPI, WebSocket, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from core.config import settings
from api import auth, transactions, budgets, ocr, categories, notifications

load_dotenv(".env")

# API documentation tags
openapi_tags = [
    {"name": "auth", "description": "Authentication and user management"},
    {"name": "transactions", "description": "CRUD operations on transactions"},
    {"name": "budgets", "description": "Budget management and alerts"},
    {"name": "categories", "description": "Category and tag filtering"},
    {"name": "ocr", "description": "Receipt OCR endpoints"},
    {"name": "notifications", "description": "Push and WebSocket notifications"},
]

# PUBLIC_INTERFACE
def create_app() -> FastAPI:
    """
    This creates the FastAPI application and registers all routers and middleware.
    """
    app = FastAPI(
        title="Personal Finance Tracker API",
        description="Backend API for personal finance tracker - auth, transactions, budgets, notifications.",
        version="0.1.0",
        openapi_tags=openapi_tags,
    )

    # CORS for local dev/mobile
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], allow_credentials=True,
        allow_methods=["*"], allow_headers=["*"],
    )

    # Register routers
    app.include_router(auth.router, prefix='/auth', tags=["auth"])
    app.include_router(transactions.router, prefix='/transactions', tags=["transactions"])
    app.include_router(budgets.router, prefix='/budgets', tags=["budgets"])
    app.include_router(categories.router, prefix='/categories', tags=["categories"])
    app.include_router(ocr.router, prefix='/ocr', tags=["ocr"])
    app.include_router(notifications.router, prefix='/notifications', tags=["notifications"])

    # WebSocket endpoint for push notifications
    @app.websocket("/ws/notifications")
    async def websocket_endpoint(websocket: WebSocket, 
                                user=Depends(auth.get_current_user_websocket)):
        """
        WebSocket endpoint for real-time budget and transaction alerts.
        Clients must connect with a valid JWT token for authentication.
        """
        await notifications.notification_ws_handler(websocket, user)

    @app.get("/ws/notifications/help", tags=["notifications"])
    async def websocket_usage_info():
        """
        Returns information on how clients can connect and use WebSocket for notifications.
        """
        return {
            "url": "/ws/notifications",
            "protocol": "websocket",
            "authentication": "Send JWT token as query param or header",
            "usage": "Receive real-time push notifications for budgets/transactions"
        }

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
