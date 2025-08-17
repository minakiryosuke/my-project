from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from pathlib import Path

app = FastAPI(title="Real Estate Support API")

# GitHub Pages からのアクセスを許可（必要に応じて追加）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://minakiryosuke.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 入口（APIの状態確認用）
@app.get("/")
def home():
    return {"ok": True, "message": "API is running"}

# （任意）Render のヘルスチェック用
@app.get("/health")
def health():
    return {"status": "ok"}

# ---------- データモデル ----------
class Professional(BaseModel):
    id: int
    name: str
    profession: str
    rating: float

class Appointment(BaseModel):
    professional_id: int
    client_name: str
    scheduled_time: datetime

class Column(BaseModel):
    id: int
    title: str
    content: str

class Community(BaseModel):
    id: int
    name: str
    description: str
    # 空リストの共有事故を避ける
    messages: List[str] = Field(default_factory=list)

# ---------- 仮のデータ ----------
professionals = [
    Professional(id=1, name="田中不動産", profession="Real Estate Agent", rating=4.5),
    Professional(id=2, name="佐藤税理士", profession="Tax Advisor", rating=4.7),
]

columns = [
    Column(id=1, title="住宅ローン控除について", content="住宅ローン控除の基本を解説します。"),
    Column(id=2, title="資産価値を高めるリフォーム", content="リフォームのポイントを紹介します。"),
]

communities = [
    Community(id=1, name="リフォーム情報交換", description="リフォームのアイデアを共有するコミュニティ"),
    Community(id=2, name="資産運用", description="不動産の資産運用について議論するコミュニティ"),
]

appointments: List[Appointment] = []

# ---------- エンドポイント ----------
@app.get("/professionals", response_model=List[Professional])
def list_professionals():
    return professionals

class AppointmentRequest(BaseModel):
    client_name: str
    scheduled_time: datetime

@app.post("/professionals/{professional_id}/appointments", response_model=Appointment, status_code=201)
def create_appointment(professional_id: int, request: AppointmentRequest):
    professional = next((p for p in professionals if p.id == professional_id), None)
    if not professional:
        raise HTTPException(status_code=404, detail="Professional not found")
    appointment = Appointment(
        professional_id=professional_id,
        client_name=request.client_name,
        scheduled_time=request.scheduled_time
    )
    appointments.append(appointment)
    return appointment

@app.get("/columns", response_model=List[Column])
def list_columns():
    return columns

@app.get("/communities", response_model=List[Community])
def list_communities():
    return communities

class MessageRequest(BaseModel):
    message: str

@app.post("/communities/{community_id}/messages", status_code=201)
def post_message(community_id: int, request: MessageRequest):
    community = next((c for c in communities if c.id == community_id), None)
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    community.messages.append(request.message)
    return {"status": "ok", "community_id": community_id, "message": request.message}

# ---------- 静的ファイル（任意・共存のため /web に配置） ----------
# Render 側で /app/static 配下にファイルを置けば /web で配信されます。
BASE_DIR = Path(__file__).resolve().parent
(app.mount("/web", StaticFiles(directory=BASE_DIR / "static", html=True), name="static"))
