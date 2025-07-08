# Backend setup:

cd fastapi-backend
python3 -m venv venv
source venv/bin/activate (Ubuntu)
pip install -r requirements.txt
prisma generate
prisma db push
uvicorn main:app --reload --host 0.0.0.0 --port 8000


# Frontend setup:

pnpm install
pnpm dev