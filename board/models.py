from django.db import models
import requests
from django.utils.dateparse import parse_date
import json
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=400)
    category = models.CharField(max_length=200)
    score = models.IntegerField("Score")
    ask_date = models.DateField("Date asked")
    
    def __str__(self):
        return self.question_text
    
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=400)
    
    def __str__(self):
        return self.answer_text

def get_categories():
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
def get_data():
    offset = 0
    while(True):
        if offset % 10000 == 0:
            print(offset)
        url = 'http://jservice.io/api/clues/?offset=' + str(offset) 
        r = requests.get(url)
        info = r.json()
        if info == []:
            break
        for question in info:
            try:
                q_text = question['question']
                if not q_text:
                    continue
                a_text =  question['answer']
                if not a_text:
                    continue
                value = question['value']
                airdate = question['airdate'].split('T')[0]
                cat = question['category']['title'].title()
                airdate = parse_date(airdate)
                
                if not value:
                    continue
                q = Question(question_text = q_text, score = value, category = cat, ask_date = airdate)
                q.save()
                q.answer_set.create(answer_text = a_text)
            except:
                continue
        offset += 100