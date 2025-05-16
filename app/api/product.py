from fastapi import APIRouter, Depends  
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.forms import ProductCreate, ProductOut

router = APIRouter()

@router.post("/products/", response_model=ProductOut)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db)):
    from app.crud.product import ProductCRUD
    product_service = ProductCRUD(db)
    return product_service.create(product=product)

@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    from app.crud.product import ProductCRUD
    product_service = ProductCRUD(db)
    return product_service.get(product_id=product_id)

@router.get("/products/")
def get_all_products(db: Session = Depends(get_db)):
    from app.crud.product import ProductCRUD
    product_service = ProductCRUD(db)
    return product_service.get_all()

@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db)):
    from app.crud.product import ProductCRUD
    product_service = ProductCRUD(db)
    return product_service.update(product_id=product_id, product=product)

@router.delete("/products/{product_id}", response_model=ProductOut)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    from app.crud.product import ProductCRUD
    product_service = ProductCRUD(db)
    return product_service.delete(product_id=product_id)
