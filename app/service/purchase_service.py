from app.crud.product import ProductCRUD
from app.schemas.logics import PurchaseCreate, PurchaseOut
from app.models.questions import Purchase
from sqlalchemy.orm import Session

class PurchaseService:
    def __init__(self, db: Session):
        self.db = db
        self.product_crud = ProductCRUD(db)

    async def calculate_total_price(self, product_id: int, quantity: int) -> int:
        product =await self.product_crud.get(product_id)
        if not product:
            raise ValueError("Product not found")
        return product.prod_price * quantity
    
    async def calculate_total_purchase_by_user(self, user_id: int):
        purchases =await self.db.query(Purchase).filter(Purchase.user_id == user_id).all()

        purchase_summary = []
        total_value = 0

        for purchase in purchases:
            product_info = {
                "product_id": purchase.product_id,
                "quantity": purchase.quantity,
                "total_price": purchase.total_price
            }

            product = self.product_crud.get(purchase.product_id)
            if product:
                product_info.update({
                    "product_name": product.prod_name,
                    "unit_price": product.prod_price
                })
            else:
                product_info.update({
                    "product_name": "Unknown",
                    "unit_price": 0
                })

            total_value += purchase.total_price
            purchase_summary.append(product_info)

        return {
            "purchases": purchase_summary,
            "total_purchase_value": total_value
        }
    
    
