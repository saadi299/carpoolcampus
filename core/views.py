from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

HOW_IT_WORKS = [
    {
        "title": "Join with your school email",
        "body": "Your email domain puts you in your organization automatically.",
    },
    {
        "title": "Add your timetable and postal code",
        "body": "We only use the first part of your postal code to find people nearby.",
    },
    {
        "title": "Get matched and share the ride",
        "body": "See classmates near you with similar schedules and send a carpool request.",
    },
]


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html", {"steps": HOW_IT_WORKS})


def about(request: HttpRequest) -> HttpResponse:
    """Explains who CarpoolCampus is for, matching logic, and privacy commitments."""
    return render(request, "core/about.html")


def health(request: HttpRequest) -> JsonResponse:
    """Lightweight check used by CI and hosting platforms."""
    return JsonResponse({"status": "ok"})
