from fastapi import APIRouter
from app.api.v1.endpoints import auth, protection, twilio, analysis

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(protection.router, prefix="/protection", tags=["protection"])
api_router.include_router(twilio.router, prefix="/twilio", tags=["twilio"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
