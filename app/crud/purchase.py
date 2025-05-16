from sqlalchemy.orm import Session
from app.models.questions import Purchase
from app.schemas.logics import PurchaseCreate, PurchaseOut
from app.service.purchase_service import PurchaseService


class PurchaseCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, purchase: PurchaseCreate):
        purchase_service = PurchaseService(self.db)
        total_price = purchase_service.calculate_total_price(
            product_id=purchase.product_id,
            quantity=purchase.quantity
        )
        db_purchase = Purchase(
            user_id=purchase.user_id,
            product_id=purchase.product_id,
            quantity=purchase.quantity,
            total_price=total_price
        )
        self.db.add(db_purchase)
        self.db.commit()
        self.db.refresh(db_purchase)
        return db_purchase

    def get(self, purchase_id: int):
        return self.db.query(Purchase).filter(Purchase.id == purchase_id).first()
    
    def get_all(self):
        return self.db.query(Purchase).all()
    
    def update(self, purchase_id: int, purchase: PurchaseCreate):
        db_purchase = self.get(purchase_id)
        if db_purchase:
            purchase_service = PurchaseService(self.db)
            total_price = purchase_service.calculate_total_price(
                product_id=purchase.product_id,
                quantity=purchase.quantity
            )
            db_purchase.user_id = purchase.user_id
            db_purchase.product_id = purchase.product_id
            db_purchase.quantity = purchase.quantity
            db_purchase.total_price = total_price
            self.db.commit()
            self.db.refresh(db_purchase)
        return db_purchase
    
    def delete(self, purchase_id: int):
        db_purchase = self.get(purchase_id)
        if db_purchase:
            self.db.delete(db_purchase)
            self.db.commit()
        return db_purchase