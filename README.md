# calc

A small Django calculator. The page collects an expression, the server
calculates it:

```
POST /api/calc   {"expression": "2+3*4"}   ->   {"expression": "2+3*4", "result": 14}
GET  /healthz    ->   {"status": "ok"}
```

## Run in a container (recommended)

```bash
docker build -t calc .
docker run --rm -p 8000:8000 calc
```

Open http://127.0.0.1:8000

## Run locally (needs Python 3.10+)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd app
python manage.py runserver
```
