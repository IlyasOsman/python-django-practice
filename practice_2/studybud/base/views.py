from django.shortcuts import render
from .models import Room

# Create your views here.

def home(request):
    rooms = Room.object.all()
    return render(request, rooms)