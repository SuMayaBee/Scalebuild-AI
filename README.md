# Backend setup

### Backend Setup

```bash
cd fastapi-backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
prisma generate
prisma db push
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

# Frontend setup

### Frontend Setup

```bash
cd presentation-ai
pnpm install
pnpm dev
```