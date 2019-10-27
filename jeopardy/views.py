from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    #last_questions = Question.objects.order_by('-ask_date')[:5]
    #context = {'latest_questions_list': last_questions}
    return render(request, 'board/index.html')