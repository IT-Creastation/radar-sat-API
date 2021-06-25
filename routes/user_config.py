from fastapi import APIRouter, Depends
from services.auth_services import get_current_user

router = APIRouter(
                    tags=["UserConfig"],
                    prefix="/users",
                    dependencies=[Depends(get_current_user)]
                )


@router.get("/{id}/config")
def get_user_config():
    return 'qsdf'
