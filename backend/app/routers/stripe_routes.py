from fastapi import APIRouter, Request
from app.config import STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET
import stripe

router = APIRouter(prefix="/stripe", tags=["Stripe"])

stripe.api_key = STRIPE_SECRET_KEY

@router.post("/create-checkout")
async def create_checkout():
    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{
            "price": "price_your_price_id",
            "quantity": 1,
        }],
        success_url="https://your-frontend/success",
        cancel_url="https://your-frontend/cancel",
    )
    return {"url": session.url}
