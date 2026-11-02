
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.incidents import get_db
from app.database.models import Resource
from app.schemas.resource import ResourceCreate, ResourceResponse

router = APIRouter(prefix="/api/v1/resources", tags=["Resources"])


@router.post("", response_model=ResourceResponse, status_code=201)
def create_resource(
    payload: ResourceCreate,
    db: Session = Depends(get_db),
):
    resource = Resource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource


@router.get("", response_model=list[ResourceResponse])
def list_resources(db: Session = Depends(get_db)):
    return db.query(Resource).order_by(Resource.id).all()
