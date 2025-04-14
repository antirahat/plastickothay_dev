from django.shortcuts import render, HttpResponse

def home (request):
    return render(request, "plastickothay/index.html")