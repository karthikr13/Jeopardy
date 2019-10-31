from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Question
from django.utils.dateparse import parse_date
import random
# Create your views here.

def index(request):
    return render(request, 'board/index.html')

def search(request, search_string):
    split_search = search_string.split('&')
    terms = [None, None, None, None]
    for i, term in enumerate(split_search):
        terms[i] = term.split('=')[1]
        if not terms[i]:
            terms[i] = 'All'
    matches = Question.objects.all()
    header = ''
    if terms[0] != 'All':
        matches = matches.filter(category__iexact = terms[0])
        header += terms[0].title()
    else:
        header += 'All questions'
    if terms[1] != 'All':
        matches = matches.filter(score__exact = terms[1])
        header += ' for ' + terms[1]
    else:
        header += ' for any points'
    if terms[2] != 'All':
        header += ', asked after ' + terms[2]
        terms[2] = parse_date(terms[2])
        matches = matches.filter(ask_date__gte = terms[2])
        asked = True
    else:
        asked = False
    if terms[3] != 'All':
        if asked:
            header += ' and before ' + terms[3]
        else:
            header += ', asked before' + terms[3]
        terms[3] = parse_date(terms[3])
        matches = matches.filter(ask_date__lte = terms[3])

    paginator = Paginator(matches, 25)
    try:
        page = request.GET.get('page')
        results = paginator.get_page(page)
        return render(request, 'board/category_sort.html', {'header': header, 'matches': results})
    except:
        return render(request, 'board/category_sort.html', {'header': header, 'matches': None})
def sort_rows(x):
    if not x:
        return 10000
    return x.score
'''
clean(col): method to ensure scores displayed in gameboard are unique and consistent across columns
sometimes, questions collected may be of same value, leading to scores in a column such as [100, 100, 200, 300, 400]
sometimes, daily double rounds get combined with regular rounds, so some columns are multiples of 200 while others are multiples of 100
col: column to clean
returns cleaned column
'''
def clean(col):
    i = 1
    for question in col:
        if not question:
            break
        question.score = i * 100
        i += 1
    return col
def gameboard(request):
    questions = [None] * 25
    header = "Categories:"
    cats = []
    for i in range(0, 5):
        question = None
        while not question:
            try:
                question = Question.objects.filter(pk__exact = random.randint(0, Question.objects.count()))[0]
            except:
                question = None
        cat = question.category
        cats.append(cat)
        header += " " + cat + ","
        matches = Question.objects.filter(category__iexact = cat)[:5]
        
        for j, match in enumerate(matches):
            questions[i*5+j] = match
        
    header = header[:-1]
    col1 = clean(sorted(questions[0:5], key = lambda x: sort_rows(x)))
    col2 = clean(sorted(questions[5:10], key = lambda x: sort_rows(x)))
    col3 = clean(sorted(questions[10:15], key = lambda x: sort_rows(x)))
    col4 = clean(sorted(questions[15:20], key = lambda x: sort_rows(x)))
    col5 = clean(sorted(questions[20:25], key = lambda x: sort_rows(x)))
    
    row1 = [col1[0], col2[0], col3[0], col4[0], col5[0]]
    row2 = [col1[1], col2[1], col3[1], col4[1], col5[1]]
    row3 = [col1[2], col2[2], col3[2], col4[2], col5[2]]
    row4 = [col1[3], col2[3], col3[3], col4[3], col5[3]]
    row5 = [col1[4], col2[4], col3[4], col4[4], col5[4]]

    '''
    row1 = sorted(questions[0:5], key = lambda x: sort_rows(x))
    row2 = sorted(questions[5:10], key = lambda x: sort_rows(x))
    row3 = sorted(questions[10:15], key = lambda x: sort_rows(x))
    row4 = sorted(questions[15:20], key = lambda x: sort_rows(x))
    row5 = sorted(questions[20:25], key = lambda x: sort_rows(x))
    '''
    return render(request, 'board/gameboard.html', {'header': header, 'cats': cats, 'row1': row1, 'row2': row2, 'row3': row3, 'row4': row4, 'row5': row5})

def random_question(request):
    question = get_object_or_404(Question, pk=random.randint(0, Question.objects.count()))
    return render(request, 'board/random.html', {'question': question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'board/detail.html', {'question': question})