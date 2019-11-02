from django.shortcuts import render, get_object_or_404
import random, requests, json
from django.utils.dateparse import parse_date
from .models import Question
#Defines backend of each URL

#global vars
off = 0 #tracks offset necessary for future API hits

def index(request):
    '''homepage'''
    return render(request, 'board/index.html')

def search_no_page(request, search_string):
    '''queries will go here without a page number, treat as if page_number = 1'''
    return search(request, search_string, 1)

def search(request, search_string, page_number):
    '''
    hits API to get query results
    pagination controlled through page_number and offset variance
    '''
    global off
    header = "Results for: "
    categories = None
    with open('categories.json') as json_file:
        categories = json.load(json_file)
    if page_number == 1:
        off = 0
    url = 'http://jservice.io/api/clues?'
    terms = ["", "", "", ""]
    split_search = search_string.split('&')
    for i, term in enumerate(split_search):
        try:
            terms[i] = term.split('=')[1]
            if not terms[i]:
                terms[i]=""
        except:
            terms[i]=""
    #The jservice API date function works strangely
    #If both min_date and max_date are provided, it works as expected
    #But if only one is provided, it works opposite of expected
    category, value, min_date, max_date = terms
    if category != "":
        category = category.lower()
        header += category + " for "
        try:
            category = categories[category]
        except:
            category = -1
    else:
        category = ""
        header += "Any category for "
    if value != "All":
        header += value + " points"
    else:
        header += "any point value"
        value = ""

    #get 100 results, take 25 first valid results, and increment number of illegal elements such that next query starts from the next 25 valid elements
    offset = (page_number-1) * 25 + off
    min_check = False
    if min_date != "":
        header += ", asked after " + min_date
        min_check = True
    if max_date != "":
        if min_check:
            header += " and before " + max_date
        else:
            header += ", asked before " + max_date
    if min_date != '""' and max_date == "":
        max_date = min_date
        min_date = ""
    elif max_date != '""' and min_date == "":
        min_date = max_date
        max_date = ""

    #empty backend DB on new page to avoid Heroku overflow on large queries
    if Question.objects.count() > 500:
        for q in Question.objects.all()[0:25]:
            q.delete()
    #hit API
    url+='category=' + str(category) + '&value='+str(value) + '&min_date=' + min_date + '&max_date=' + max_date + '&offset=' + str(offset)
    data =requests.get(url).json()
    questions=[None]*25
    i = 0
    next_flag = None
    for question in data:
        try:
            q_text = question['question']
            a_text = question['answer']
            score = question['value']
            airdate=question['airdate'].split('T')[0]
            airdate=parse_date(airdate)
            #print()
            category = question['category']['title']
            if None in [q_text, a_text, score, airdate, category] or score == 0:
                continue
            #single quotes in question or answer mess with Javascript
            q_text = q_text.replace("&#39;", '')
            a_text = a_text.replace("&#39;", '')
            q_text = q_text.replace("'", '')
            a_text = a_text.replace("'", '')

            if i < 25:
                print(q_text, a_text, score, airdate, category)
                q  = Question(question_text=q_text, category = category, score = score, ask_date = airdate, answer_text = a_text)
                print(q)
                questions[i] = q
                q.save()
            if i >= 25:
                #check if there is a next page
                next_flag = page_number+1
                break
            i += 1
        #hit if broken format on question
        except:
            break

    #check if there is a previous page
    prev_flag = None
    if page_number != 1:
        prev_flag = page_number-1
    print(questions)
    #allow for table entry in HTML
    row1 = questions[0:5]
    row2 = questions[5:10]
    row3 = questions[10:15]
    row4 = questions[15:20]
    row5 = questions[20:25]
    return render(request, 'board/category_sort.html', {'header': header, 'matches': questions, 'prev': prev_flag, 'next': next_flag, 'row1': row1, 'row2': row2, 'row3': row3, 'row4': row4, 'row5':row5})

def gameboard(request):
    '''create gameboard of questions from random categories'''
    if Question.objects.count() > 500:
        for q in Question.objects.all()[0:25]:
            q.delete()
    questions = [None] * 25
    header = "Categories:"
    cats = []
    categories = {}
    with open('categories.json') as json_file:
        categories = json.load(json_file)

    #randomly select categories that have enough questions to be used
    for i in range(0, 5):
        question = None
        cat = None
        generated = None
        while not cat:
            index = random.randint(0, len(categories))
            cat = list(categories.keys())[index]
            cat_id = categories[cat]
            url = 'http://jservice.io/api/category?id='+str(cat_id)
            r  = requests.get(url)
            generated = r.json()
            if generated['clues_count'] < 5:
                cat = None
                continue
            cats.append(cat)
        matches = set()
        j = 0
        for question in generated['clues']:
            q_text = question['question']
            a_text = question['answer']
            score = question['value']
            airdate=question['airdate'].split('T')[0]
            airdate=parse_date(airdate)
            category = cat
            if None in [q_text, a_text, score, airdate, category] or score == 0:
                continue
            q_text = q_text.replace("&#39;", '')
            a_text = a_text.replace("&#39;", '')
            q_text = q_text.replace("'", '')
            a_text = a_text.replace("'", '')
            q = Question(question_text=q_text, score=score, ask_date=airdate, category=category, answer_text=a_text)   
            q.save()
            matches.add(q)
            if len(matches) >= 5:
                break
            j += 1
        matches = list(matches)
        while len(matches) < 5:
            matches.append(None)
        for j, match in enumerate(matches):
            questions[i*5+j] = match

    #sort columns
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
    return render(request, 'board/gameboard.html', {'header': header, 'cats': cats, 'row1': row1, 'row2': row2, 'row3': row3, 'row4': row4, 'row5': row5})

def random_question(request):
    '''randomly generate a single question'''
    if Question.objects.count() > 500:
        for q in Question.objects.all()[0:25]:
            q.delete()
    question = None
    url = 'http://jservice.io/api/random'
    r  = requests.get(url)
    generated = r.json()[0]
    while not question:
        
        q_text = generated['question']
        a_text = generated['answer']
        score = generated['value']
        airdate = generated['airdate'].split('T')[0]
        airdate = parse_date(airdate)
        category = generated['category']['title']
        if None in [q_text, a_text, score, airdate, category] or score == 0:
            r  = requests.get(url)
            generated = r.json()[0]
            continue
        q_text = q_text.replace("&#39;", '')
        a_text = a_text.replace("&#39;", '')
        q_text = q_text.replace("'", '')
        a_text = a_text.replace("'", '')
        question = Question(question_text=q_text, score=score, ask_date=airdate, category=category, answer_text=a_text)
        question.save()
    return render(request, 'board/random.html', {'question': question})
    print(question)

def detail(request, question_id):
    '''Displays question/answer pairing'''
    try:
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'board/detail.html', {'question': question})
    except:
        return render(request, 'board/detail.html', {'question': None})

#non-user facing methods
def sort_rows(x):
    '''ensures blank squares at bottom'''
    if not x:
        return 10000
    return int(x.score)

def clean(col):
    '''
    clean(col): method to ensure scores displayed in gameboard are unique and consistent across columns
    sometimes, questions collected may be of same value, leading to scores in a column such as [100, 100, 200, 300, 400]
    sometimes, daily double rounds get combined with regular rounds, so some columns are multiples of 200 while others are multiples of 100
    col: column to clean
    returns cleaned column
    '''
    i = 1
    for question in col:
        if not question:
            break
        question.score = i * 100
        i += 1
    return col

def get_categories():
    '''
    one time method call by developer that creates categories.json, which maps category strings to category ids used by jservice.io
    '''
    offset = 0
    cats = {}
    while True:
        url = 'http://jservice.io/api/categories/?count=100&offset=' + str(offset)
        r  = requests.get(url)
        info = r.json()
        if info == []:
            break
        for cat in info:
            cat_id = cat['id']
            cat_name = cat['title']
            cats[cat_name] = cat_id
        offset += 100
    cat_json = json.dumps(cats)
    f = open("board/dict.json", "w")
    f.write(cat_json)
    f.close()