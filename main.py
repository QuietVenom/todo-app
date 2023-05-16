import models
from company import companyapis, dependencies
from database import engine
from fastapi import Depends, FastAPI
from routers import address, auth, todos, users
from starlette import status
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/todos/", status_code=status.HTTP_302_FOUND)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
# app.include_router(address.router)
# app.include_router(
#     companyapis.router,
#     prefix="/companyapis",
#     tags=["companyapis"],
#     dependencies=[Depends(dependencies.get_token_header)],
#     responses={418: {"description": "Internal Use Only"}},
# )
