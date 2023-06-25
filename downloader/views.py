from django.shortcuts import render
from django.http import HttpResponse


def ConvertVideoPageViews(request):
    return render(request, "ytb_download.html")

