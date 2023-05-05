from data.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from .form import LoginForm


def index(request):
    return render(request, "index.html")


def login(request):
    context = {"form": LoginForm()}

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            if User.objects.filter(**form.cleaned_data).exists():  # 如果能够在数据库中找到记录
                return redirect(reverse("index"))  # 跳转主页
            else:
                context.update(
                    {
                        "is_error": True,
                        "error_msg": "用户名或密码错误",
                    }
                )
        else:
            context.update(
                {
                    "is_error": True,
                    "error_msg": "格式错误",
                }
            )

    return render(request, "login.html", context)


def hello(request):
    return redirect(reverse("index"))
