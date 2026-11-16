import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.html import format_html
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .engine import CalcError, evaluate


@require_GET
def index(request):
    footer = format_html("Practice app for <b>{}</b>", "DEV-017 DevOps Basics")
    return render(request, "calculator/index.html", {"footer": footer})


@csrf_exempt
@require_POST
def calculate(request):
    """POST {"expression": "2+3*4"} -> {"expression": "2+3*4", "result": 14}"""
    try:
        expression = json.loads(request.body or b"{}")["expression"]
    except (ValueError, KeyError, TypeError):
        return JsonResponse(
            {"error": 'Send JSON like {"expression": "2+3*4"}'}, status=400
        )
    try:
        result = evaluate(expression)
    except CalcError as exc:
        return JsonResponse({"expression": expression, "error": str(exc)}, status=400)
    return JsonResponse({"expression": expression, "result": result})


@require_GET
def healthz(request):
    """Liveness/readiness check for Docker HEALTHCHECK and Kubernetes probes."""
    return JsonResponse({"status": "ok"})
