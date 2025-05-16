from sqlalchemy.orm import Session
from app.models.forms import Product
from app.schemas.forms import ProductCreate,ProductOut

class ProductCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, product: ProductCreate):
        db_product = Product(prod_name=product.prod_name, prod_price=product.prod_price)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def get(self, product_id: int):
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_by_prod_name(self, prod_name: str):
        return self.db.query(Product).filter(Product.prod_name == prod_name).first()
    
    def get_all(self):
        return self.db.query(Product).all()
    
    def update(self, product_id: int, product: ProductCreate):
        db_product = self.get(product_id)
        if db_product:
            db_product.prod_name = product.prod_name
            db_product.prod_price = product.prod_price
            self.db.commit()
            self.db.refresh(db_product)
        return db_product
    
    def delete(self, product_id: int):
        db_product = self.get(product_id)
        if db_product:
            self.db.delete(db_product)
            self.db.commit()
        return db_product
