# calc

A small Django calculator. The page collects an expression, the server
calculates it:

```
POST /api/calc   {"expression": "2+3*4"}   ->   {"expression": "2+3*4", "result": 14}
```

Run it locally:

```bash
cd app
python manage.py runserver
```

Open http://127.0.0.1:8000
