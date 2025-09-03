from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.core.security import validate_access_token
from jose import JWTError


templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

def get_current_user_from_cokie(request: Request):
    token= request.cookies.get("access_token")
    if not token:
        return None
    try:
        payload = validate_access_token(token)
        return payload.get("sub")
    except JWTError:
        return None


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request":request})

@router.get("/register", response_class = HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html",{"request": request})

@router.get("/",response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("base.html", {"request":request})
