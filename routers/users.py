import sys

sys.path.append("..")

import models
from database import SessionLocal, engine
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from .auth import get_current_user, get_password_hash, verify_password

router = APIRouter(
    prefix="/users", tags=["users"], responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get("/edit-password", response_class=HTMLResponse)
async def edit_user_view(request: Request):
    user = await get_current_user(request)

    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse(
        "edit-user-password.html", {"request": request, "user": user}
    )


@router.post("/edit-password", response_class=HTMLResponse)
async def user_password_change(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    db: Session = Depends(get_db),
):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    user_data = db.query(models.Users).filter(models.Users.username == username).first()

    msg = "Invalid username or password"

    if user_data is not None:
        if username == user_data.username and verify_password(
            password, user_data.hashed_pss
        ):
            user_data.hashed_pss = get_password_hash(password2)
            db.add(user_data)
            db.commit()
            msg = "Password updated"

    return templates.TemplateResponse(
        "edit-user-password.html", {"request": request, "user": user, "msg": msg}
    )


# class UserVerification(BaseModel):
#     username: str
#     password: str
#     new_password: str


# @router.get("/")
# async def read_all(db: Session = Depends(get_db)):
#     return db.query(models.Users).all()


# @router.get("/user/{user_id}")
# async def user_by_path(user_id: int, db: Session = Depends(get_db)):
#     user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
#     if user_model is not None:
#         return user_model
#     return 'Invalid User ID'


# @router.get("/user/")
# async def user_by_query(user_id: int, db: Session = Depends(get_db)):
#     user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
#     if user_model is not None:
#         return user_model
#     return 'Invalid User ID'


# @router.put("/user/password")
# async def user_pss_change(user_verification: UserVerification, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()

#     user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

#     if user_model is not None:
#         if user_verification.username == user_model.username and verify_password(user_verification.password, user_model.hashed_pss):
#             user_model.hashed_pss = get_password_hash(user_verification.new_password)
#             db.add(user_model)
#             db.commit()
#             return 'Successful'
#     return 'Invalid user or request'


# @router.delete("/user")
# async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
#     if user is None:
#         raise get_user_exception()

#     user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

#     if user_model is None:
#         return 'Invalid user or request'

#     db.query(models.Users).filter(models.Users.id == user.get('id')).delete()
#     db.commit()
#     return 'Delete Successful'
