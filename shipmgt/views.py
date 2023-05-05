from django.forms.models import model_to_dict
from data.models import *
from django.shortcuts import render
from django.utils import timezone
from .forms import *


def delivery_create(request):
    context = {"form": DelSaveForm()}

    if request.method == "POST":
        form1 = DelInqueryForm(request.POST)
        if form1.is_valid():
            # 查询订单号是否存在
            data = form1.cleaned_data

            if data["DelOrdNum"] == "":
                context.update(
                    {
                        "is_error": True,
                        "error_msg": "请输入订单号！",
                    }
                )
            else:
                if len(data["DelOrdNum"]) != 9:
                    context.update(
                        {
                            "is_error": True,
                            "error_msg": "请输入正确的订单号！",
                        }
                    )
                else:
                    if "DelOrdNum" in data:
                        data["DelOrdNum"] = int(data["DelOrdNum"][1:])
                    order_qs = Order.objects.filter(OrdNum=data["DelOrdNum"])
                    if order_qs.exists():
                        # 创建
                        order = Order.objects.get(pk=data["DelOrdNum"])

                        if order.IsPost == 0:

                            form = DelSaveForm(data)
                            print(request.POST)
                            if form.is_valid():
                                delivery = form.save()
                                order.IsPost = 1
                                order.save()
                                context.update(
                                    {
                                        "is_suc": True,
                                        "delivery": delivery,
                                    }
                                )
                            else:
                                context.update(
                                    {
                                        "is_error": True,
                                        "error_msg": "格式错误",
                                    }
                                )
                        else:
                            context.update(
                                {
                                    "is_error": True,
                                    "error_msg": "该订单已发货",
                                }
                            )

                    else:
                        context.update(
                            {
                                "is_error": True,
                                "error_msg": "该订单不存在",
                            }
                        )

        else:

            context.update(
                {
                    "is_error": True,
                    "error_msg": "格式有误",
                }
            )

    return render(request, "ship/delivery_create.html", context)


def delivery_inquery(request):
    context = {"form": DelInqueryForm()}

    if request.method == "POST":
        form = DelInqueryForm(request.POST)

        if form.is_valid():

            data = form.cleaned_data
            data = {
                key: value
                for key, value in data.items()
                if value != "" and value != None
            }
            flag = 0
            if "DelNum" in data:
                if len(data["DelNum"]) != 9:
                    flag = 1
                else:
                    data["DelNum"] = int(data["DelNum"][1:])
            if "DelOrdNum" in data:
                if len(data["DelOrdNum"]) != 9:
                    flag = 1
                else:
                    data["DelOrdNum"] = int(data["DelOrdNum"][1:])

            print(data)

            delivery_qs = Delivery.objects.filter(**data)
            if flag != 1:
                if delivery_qs.exists():
                    context.update(
                        {
                            "is_suc": True,
                            "delivery_qs": delivery_qs,
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
    return render(request, "ship/delivery_inquery.html", context)


def delivery_modify(request, DelNum):
    delivery = Delivery.objects.get(pk=DelNum)

    context = {"form": DelModifyForm(model_to_dict(delivery)), "delivery": delivery}

    if request.method == "POST":
        form = DelModifyForm(request.POST, instance=delivery)
        if form.is_valid():
            form.save()
            context.update(
                {
                    "is_suc": True,
                    "delivery": delivery,
                    "form": DelModifyForm(model_to_dict(delivery)),
                }
            )
        else:
            context.update(
                {
                    "is_error": True,
                    "error_msg": "格式有误",
                }
            )

    return render(request, "ship/delivery_modify.html", context)


def delivery_detail(request, DelNum):
    delivery = Delivery.objects.get(pk=DelNum)
    context = {"delivery": delivery}
    return render(request, "ship/delivery_detail.html", context)


def check_stock(request):
    context = {"form": CheckStockForm()}

    if request.method == "POST":
        form = CheckStockForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data
            data = {
                key: value
                for key, value in data.items()
                if value != "" and value != None
            }
            if "MatNum" in data:
                data["MatNum"] = int(data["MatNum"][1:])
            if "DelOrdNum" in data:
                data["DelOrdNum"] = int(data["DelOrdNum"][1:])
            print(data)

            Material_qs = Material.objects.filter(**data)
            if Material_qs.exists():
                context.update(
                    {
                        "is_suc": True,
                        "Material_qs": Material_qs,
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

    return render(request, "ship/check_stock.html", context)


def check_stock_detail(request, MatNum):
    Mat = Material.objects.get(pk=MatNum)
    context = {"Material": Mat}

    return render(request, "ship/check_stock_detail.html", context)


def post(request):
    context = {"form": PostForm()}
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data["DelNum"] = int(data["DelNum"][1:])
            try:
                delivery = Delivery.objects.get(pk=data["DelNum"])
            except Exception:
                context.update(
                    {
                        "is_error": True,
                        "error_msg": "该发货单不存在",
                    }
                )
            else:
                if delivery is not None and delivery.PostDate is None:
                    delivery.PostDate = timezone.now()
                    delivery.save()
                    context.update(
                        {
                            "is_suc": True,
                            "delivery": delivery,
                        }
                    )
                else:
                    context.update(
                        {
                            "is_error": True,
                            "error_msg": "该发货单已发货",
                        }
                    )

        else:
            context.update(
                {
                    "is_error": True,
                    "error_msg": "格式有误",
                }
            )

    return render(request, "ship/post.html", context)
