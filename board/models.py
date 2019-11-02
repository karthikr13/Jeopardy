from django.db import models
# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=400)
    category = models.CharField(max_length=200)
    score = models.IntegerField("Score")
    ask_date = models.DateField("Date asked")
    answer_text = models.CharField(max_length=400)
    def __str__(self):
        return self.question_text