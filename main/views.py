from django.contrib import auth
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import LoginForm, SignUpForm, QuizForm, QuestionForm, ChoiceForm
from .models import Quiz, Choice, QuizAnswer, QuizInformation
from django.db.models import Avg, Q

# Create your views here.
def index(request):
    return render(request, "main/index.html")


def signup(request):
    if request.method == "GET":
        form = SignUpForm()
    elif request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)

            return redirect("index")

    context = {"form": form}
    return render(request, "main/signup.html", context)


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm  
    template_name = "main/login.html" 

def home(request):
    return render(request, 'main/home.html')

@login_required # ログインしている場合にビュー関数を実行する
def create_quiz(request):
    if request.method == "GET":
        quiz_form = QuizForm()
    elif request.method == "POST":
        # 送信内容の取得
        quiz_form = QuizForm(request.POST)
        # 送信内容の検証
        if quiz_form.is_valid():
            quiz = quiz_form.save(commit=False)
            # クイズ作成者を与えて保存
            user = request.user
            quiz.user = user
            quiz.save()
            # 質問作成画面に遷移する
            return redirect("create_question", quiz.id)
    context = {
        "quiz_form":quiz_form,
    }
    return render(request, "main/create_quiz.html", context)

@login_required
def create_question(request, quiz_id):
    # Quiz オブジェクトから id が前画面で作成したオブジェクトの id に等しいものを取得する
    quiz = get_object_or_404(Quiz, id=quiz_id)
    # 現在データベースに保存されている質問の数
    current_question_num = quiz.question_set.all().count()
    # 次に質問を作成した際にデータベースに保存される質問の数
    next_question_num = current_question_num + 1
    if request.method == "GET":
        question_form = QuestionForm()
        choice_form = ChoiceForm()
    elif request.method == "POST":
        # 送信内容の取得
        question_form = QuestionForm(request.POST)
        # 送信された 4 つの選択肢のテキストを取得
        choices = request.POST.getlist("choice")
        # 正解選択肢の id を取得
        answer_choice_num = request.POST["is_answer"]
        # 送信内容の検証
        if question_form.is_valid():
            question = question_form.save(commit=False)
            # 送信内容を保存する
            question.quiz = quiz
            question.save()
            # Choice モデルにデータを保存する
            for i, choice in enumerate(choices):
                # 正解選択肢には is_answer を True にして保存する
                if i == int(answer_choice_num):
                    Choice.objects.create(
                        question=question, choice=choice, is_answer=True
                    )
                else:
                    Choice.objects.create(
                        question=question, choice=choice, is_answer=False
                    )
            return redirect("create_question", quiz_id)
    context = {
        "question_form":question_form,
        "choice_form":choice_form,
        "quiz_id" : quiz_id,
        "next_question_num" : next_question_num,
    }
    return render(request, "main/create_question.html", context)

@login_required
def answer_quiz_list(request):
    user = request.user
    quiz_list = Quiz.objects.exclude(user=user)

    keyword = request.GET.get('keyword')
    if keyword:
        keywords = keyword.split()
        for k in keywords:
            quiz_list = quiz_list.filter(Q(title__icontains=k) | Q(description__icontains=k))
    
    context = {
        "quiz_list":quiz_list,
    }
    return render(request, "main/answer_quiz_list.html", context)

@login_required
def answer_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.question_set.all()
    score = 0

    question_num = questions.count()
    user = request.user
    if request.method == "POST":
        for question in questions:
            choice_id = request.POST.get(str(question.id))
            choice_obj = get_object_or_404(Choice, id=choice_id)
            if choice_obj.is_answer:
                score += 1

        answer_rate = score*100/question_num
        
        QuizAnswer.objects.create(
            user=user, quiz=quiz, score=score, answer_rate=answer_rate
        )

        quiz_answer = QuizAnswer.objects.filter(quiz=quiz)
        whole_average_score = quiz_answer.aggregate(Avg('score'))["score__avg"]
        whole_answer_rate = quiz_answer.aggregate(Avg('answer_rate'))["answer_rate__avg"]
        quiz_information = QuizInformation.objects.filter(quiz=quiz)

        QuizInformation.objects.update_or_create(
            quiz=quiz,
            defaults={
                "average_score":whole_average_score,
                "answer_rate":whole_answer_rate
            },
        )

        return redirect("result", quiz_id)
    context = {
        "quiz":quiz,
        "questions":questions,
    }
    return render(request, "main/answer_quiz.html", context)

@login_required
def result(request, quiz_id):
    user = request.user
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_answer = QuizAnswer.objects.filter(quiz=quiz, user=user).order_by("answered_at").last()
    context = {
        "quiz_answer":quiz_answer,
    }

    return render(request, "main/result.html", context)

@login_required
def home(request):
    user = request.user
    quiz_list = Quiz.objects.filter(user=user)
    context = {
        "quiz_list":quiz_list,
    }
    return render(request, "main/home.html", context)

@login_required
def quiz_information(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz_information = get_object_or_404(QuizInformation, quiz=quiz)
    quiz_answer = quiz.quizanswer_set.all()
    context = {
        "quiz_answer":quiz_answer,
        "quiz_information":quiz_information,
    }
    return render(request, "main/quiz_information.html", context)

class LogoutView(auth_views.LogoutView, LoginRequiredMixin):
    pass