from django.forms.models import model_to_dict
from data.models import *
from django.shortcuts import render
from .forms import *


def create(request):
    context = {
        "form": CustSaveForm(),
    }

    if request.method == "POST":
        form = CustSaveForm(request.POST)
        if form.is_valid():
            customer = form.save()
            context.update(
                {
                    "is_suc": True,
                    "customer": customer,
                }
            )
        else:
            context.update(
                {
                    "is_error": True,
                    "error_msg": "格式有误",
                }
            )
    return render(request, "customer/create.html", context)


def inquery(request):
    context = {"form": CustInqueryForm()}

    if request.method == "POST":
        form = CustInqueryForm(request.POST)
        if form.is_valid():

            # 数据规整
            data = form.cleaned_data
            data = {
                key: value
                for key, value in data.items()
                if value != "" and value != None
            }  # 去除非没填的值
            if "CustNum" in data:
                data["CustNum"] = int(data["CustNum"][1:])  # 化为整数

            print(data)

            customer_qs = Customer.objects.filter(**data)  # customer query set
            if customer_qs.exists():  # 如果能够在数据库中找到记录
                context.update(
                    {
                        "is_suc": True,
                        "customer_qs": customer_qs,
                    }
                )
            else:
                context.update(
                    {
                        "is_error": True,
                        "error_msg": "无满足条件项",
                    }
                )
        else:
            context.update(
                {
                    "is_error": True,
                    "error_msg": "格式有误",
                }
            )
    return render(request, "customer/inquery.html", context)


def detail(request, CustNum):

    customer = Customer.objects.get(pk=CustNum)
    context = {"customer": customer}

    return render(request, "customer/detail.html", context)


def modify(request, CustNum):

    customer = Customer.objects.get(pk=CustNum)

    context = {"form": CustSaveForm(model_to_dict(customer)), "customer": customer}

    if request.method == "POST":
        form = CustSaveForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            context.update(
                {
                    "is_suc": True,
                    "customer": customer,
                    "form": CustSaveForm(model_to_dict(customer)),
                }
            )
        else:
            context.update(
                {
                    "is_error": True,
                    "error_msg": "格式有误",
                }
            )

    return render(request, "customer/modify.html", context)
