from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User, Quiz, Question, Choice


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = ("username", "email")

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"

class QuizForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["class"] = "form-control"
        self.fields["description"].widget.attrs["rows"] = "3"

    class Meta:
        model = Quiz
        fields = ("title", "description")

# Question モデル
class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["question"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Question
        fields = ("question",)

# Choice モデル
class ChoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["choice"].widget.attrs["class"] = "form-control"

    class Meta:
        model = Choice
        fields = ("choice",)