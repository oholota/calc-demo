# calc

A small Django calculator, used in the DEV-017 DevOps Basics course to build
a delivery pipeline step by step. The page collects an expression, the server
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

## Tests

```bash
pip install -r requirements-dev.txt
pytest tests/unit                                      # logic only, no server
pytest tests/http --base-url http://127.0.0.1:8000     # against the running app
```

## Pipeline (`.github/workflows/pipeline.yml`)

| Job | Runs on | What it does |
|---|---|---|
| Test | every push and pull request | unit tests, builds the image, starts it, HTTP tests against the container |
| Publish | push only | pushes the tested image to GitHub Container Registry (`ghcr.io/<owner>/<repo>`) |
| Deploy | push only | creates a throwaway Kubernetes cluster (kind), deploys the image by digest, smoke test |
| AI summary | pull requests | an LLM comments the pull request with a short summary and risks |

Nothing to configure for test, publish and deploy: they use only the
built-in `GITHUB_TOKEN`.

## AI assistant (optional)

`tools/ai_assist.py` asks an LLM to explain a failed test job (the answer is
in the job summary) and to summarize pull requests (a PR comment). Any
OpenAI-compatible API works. Settings -> Secrets and variables -> Actions:

| Name | Kind | Example |
|---|---|---|
| `AI_BASE_URL` | variable | `https://<resource>.openai.azure.com/openai/v1` (Azure OpenAI), `https://api.openai.com/v1` |
| `AI_MODEL` | variable | `gpt-5-mini` (for Azure: the deployment name) |
| `AI_API_KEY` | secret | the API key |

Without them the AI steps print "not configured" and the pipeline is
unaffected. The assistant only advises: it never fails or blocks a run, and it
receives test output, app logs and the diff, never secrets.

Try it locally:

```bash
export AI_BASE_URL=... AI_MODEL=... AI_API_KEY=...
python3 tools/ai_assist.py explain test-output.log
```

`deploy-cloudrun.yml` is an optional manual workflow for a Google Cloud
project (needs `GCP_PROJECT_ID`, `GCP_REGION` variables and a `GCP_CREDENTIALS` secret).

## Course steps

The history is tagged so the demo can go one step at a time:

| Tag | Step |
|---|---|
| `step-0-app` | the app, no environment description |
| `step-1-docker` | pinned requirements, Dockerfile, health check |
| `step-2-tests` | unit and HTTP tests |
| `step-3-ci` | CI: tests and image build on every push |
| `step-4-publish` | publish the tested image to GHCR |
| `step-5-deploy` | deploy to Kubernetes with a smoke test |
| `step-6-ai` | AI assistant: explains failed runs, summarizes pull requests |
