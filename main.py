from fastapi import FastAPI, Depends, HTTPException, Request, Body
from db import Base, get_db, engine
from models.users import UserORM
from models.requests import RequestORM
from argon2 import PasswordHasher
from schemas.users import UserReg, UserLogin
from sqlalchemy.orm import Session
from schemas.request import Request_add
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key = "ключ")
ph = PasswordHasher()
templates = Jinja2Templates("templates")
def hash_password(password):
    return ph.hash(password)
def verify_password(hash,password):
    try:
        return ph.verify(hash,password)
    except:
        return False
    



@app.get("/register")
def get_register(request: Request):
    return templates.TemplateResponse(request= request, name ="register.html")

@app.get("/login")
def get_login(request: Request):
    return templates.TemplateResponse(request= request, name ="login.html")


@app.get("/request")
def get_request(request: Request):
    return templates.TemplateResponse(request= request, name ="request.html")



@app.post("/api/register")
def register(user: UserReg,db: Session = Depends(get_db) ):
    req = db.query(UserORM).filter_by(login = user.login).first()
    if req: raise HTTPException(status_code=401, detail="Данный логин уже используется")
    req = UserORM(
        login = user.login,
        password = hash_password(user.password),
        email = user.email,
        phone = user.phone,
        full_name = user.full_name
    )
    db.add(req)
    db.commit()
    return {"message":"Успешно зарегистрирован"}

@app.post("/api/login")
def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    req = db.query(UserORM).filter_by(login = user.login).first()
    if not req: raise HTTPException(status_code=401, detail="Неверный логин")
    if not verify_password(req.password, user.password): raise HTTPException(status_code=401, detail="Неверный пароль")
    request.session["user_id"] = req.id
    request.session["role"] = req.role
    return {"message":"Успешно авторизирован"}

@app.get("/admin" )
def admin(request: Request, db: Session = Depends(get_db), limit = 5, page = 1):
    count = db.query(RequestORM).count()
    req = db.query(RequestORM).limit(limit).offset((page-1)*limit).all()
    return templates.TemplateResponse(request=request, name = "admin.html", context={"data":req})


@app.post("/api/request")
def request(request: Request, req: Request_add, db: Session = Depends(get_db)):
    req = RequestORM(
        user_id = request.session.get("user_id"),
        location = req.location,
        pay = req.pay,
        date = req.date
    )
    db.add(req)
    db.commit()
    return {"message":"Успешно создано"}

@app.patch("/api/request/{id}")
def patch_request(id: int, status = Body(embed=True), db: Session = Depends(get_db)):
    req = db.query(RequestORM).filter_by(id = id).first()
    req.status = status
    db.commit()
    return {"message":"Успешно обновлено"}

