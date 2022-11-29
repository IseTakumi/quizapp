from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # 作成者
    title = models.CharField(max_length=50) # タイトル
    description = models.TextField(max_length=500) # 説明文

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE) # どのクイズに対する質問か
    question = models.CharField(max_length=100) # 質問文

    def __str__(self):
        return self.question

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # どの質問に対する選択肢か
    choice = models.CharField(max_length=200) # 選択肢
    is_answer = models.BooleanField(default=False) # 正解かどうか

    def __str__(self):
        return self.choice

class QuizAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(default=0)
    answer_rate = models.FloatField(default=0)

    def __str__(self):
        return self.score

class QuizInformation(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    average_score = models.FloatField(default=0)
    answer_rate = models.FloatField(default=0)