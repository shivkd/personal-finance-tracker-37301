from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user import User
from schemas.user import UserCreate, UserRead, Token
from core.auth import verify_password, get_password_hash, create_access_token, get_current_user_websocket
from core.database import get_db
router = APIRouter()

# Expose get_current_user_websocket for use in main.py
get_current_user_websocket = get_current_user_websocket

# PUBLIC_INTERFACE
@router.post("/register", response_model=UserRead, summary="Register new user")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    if result.scalar() is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_pw)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserRead(id=db_user.id, email=db_user.email)

# PUBLIC_INTERFACE
@router.post("/login", response_model=Token, summary="Login returning JWT token")
async def login(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar()
    if db_user is None or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    token = create_access_token({"sub": db_user.email})
    return Token(access_token=token, token_type="bearer")
