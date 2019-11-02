from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    return render(request, 'board/index.html')