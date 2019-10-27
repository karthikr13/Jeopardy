from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Question
# Create your views here.

def index(request):
    #last_questions = Question.objects.order_by('-ask_date')[:5]
    #context = {'latest_questions_list': last_questions}
    return render(request, 'board/index.html')

def search_category(request, category):
    matches = Question.objects.filter(category__iexact = category)
    paginator = Paginator(matches, 25)
    header = category.title() + ", all scores" 
    try:
        page = request.GET.get('page')
        results = paginator.get_page(page)
        return render(request, 'board/category_sort.html', {'header': header, 'matches': results})
    except:
        return render(request, 'board/category_sort.html', {'header': header, 'matches': None})

def search_category_score(request, category, score):
    matches = Question.objects.filter(category__iexact = category, score__exact = score)
    paginator = Paginator(matches, 25)
    header = category.title() + " for " + str(score) + " points" 
    try:
        page = request.GET.get('page')
        results = paginator.get_page(page)
        return render(request, 'board/category_sort.html', {'header': header, 'matches': results})
    except:
        return render(request, 'board/category_sort.html', {'header': header, 'matches': None})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'board/detail.html', {'question': question})