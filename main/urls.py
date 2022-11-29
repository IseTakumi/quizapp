from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("home/", views.home, name="home"), 
    path("create_quiz/", views.create_quiz, name="create_quiz"),
    path("create_question/<quiz_id>/", views.create_question, name="create_question"),
    path("answer_quiz_list/", views.answer_quiz_list, name="answer_quiz_list"),
    path("answer_quiz/<quiz_id>/", views.answer_quiz, name="answer_quiz"), 
    path("result/<quiz_id>/", views.result, name="result"),
    path("quiz_information/<quiz_id>", views.quiz_information, name="quiz_information"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]