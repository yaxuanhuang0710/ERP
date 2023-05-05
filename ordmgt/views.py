import json

from django.forms.widgets import NullBooleanSelect

from data.models import *
from django.forms.models import model_to_dict
from django.shortcuts import render

from .forms import *
import datetime


def create(request):
    context = {}
    if request.method == "POST":
        OM = "[" + request.POST["OM"] + "]"
        OM = json.loads(OM)

        data = {
            key: value[0]
            for key, value in dict(request.POST).items()
            if key != "OM" and key != "csrfmiddlewaretoken"
        }
        if data["PayCustNum"]!="":
            data["PayCustNum"] = int(data["PayCustNum"][1:])
        if data["RcvCustNum"]!="":
            data["RcvCustNum"] = int(data["RcvCustNum"][1:])

        form1 = OrdSaveForm(data)
        form1.OdrCreDate = datetime.date.today()  # 今天日期
        form1.IsPost = 0
        
        if form1.is_valid():
            order = form1.save()
            context.update({"is_suc": True, "new_ord": order})
            for i in range(len(OM)):
                matnum = int(OM[i]["OM_MatNum"][1:])
                mat = Material.objects.get(pk=matnum)
                OrdMat.objects.create(
                    OM_OrdNum=order,
                    OM_MatNum=mat,
                    OrdMatDesc=OM[i]["OrdMatDesc"],
                    OrdMatQty=OM[i]["OrdMatQty"],
                    OdrMatDisc=OM[i]["OdrMatDisc"],
                )
        else:
            print(form1.errors)
            context.update({"is_error": True, "error_msg": "格式有误"})
        # OM 是一个列表，其每个元素是一个物料项的信息，表现为一个字典
        # OM[0]["OM_MatNum"] 物料号 字符串，写入记录需要格式化为整数（AutoField影响）
        # OM[0]["OrdMatDesc"] 物料描述
        # OM[0]["OrdMatQty"] 物料数量
        # OM[0]["OdrMatDisc"] 物料折扣
    return render(request, "order/create.html", context)


def inquery(request):
    context = {"form1": OrdInqueryForm()}
    if request.method == "POST":
        form1 = OrdInqueryForm(request.POST) 
        if form1.is_valid():
            # 数据规整
            data1 = form1.cleaned_data
            data1 = {
                key: value
                for key, value in data1.items()
                if value != "" and value != None
            }  # 去除非没填的值
            
            if "OrdNum" in data1:
                data1["OrdNum"] = int(data1["OrdNum"][1:])
            if "PayCustNum" in data1:
                data1["PayCustNum"] = int(data1["PayCustNum"][1:])  # 化为整数
            if "RcvCustNum" in data1:
                data1["RcvCustNum"] = int(data1["RcvCustNum"][1:])  # 化为整数
           
            order_qs = Order.objects.filter(**data1)  # customer query set
            
            if order_qs.exists():  # 如果能够在数据库中找到记录
                context.update(
                    {
                        "is_suc": True,
                        "order_qs": order_qs,
                    }
                )
            else:
                print("没有满足项")
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
    return render(request, "order/inquery.html", context)


def modify(request, OrdNum):
    order = Order.objects.get(pk=OrdNum)
    ordmat_qs = OrdMat.objects.filter(OM_OrdNum=OrdNum)
    context = {
        "form1": OrdSaveForm(model_to_dict(order)),
        "order": order,
        "ordmat_qs": ordmat_qs,
    }

    if request.method == "POST":
        OM = "[" + request.POST["OM"] + "]"
        OM = json.loads(OM)

        data = {
            key: value[0]
            for key, value in dict(request.POST).items()
            if key != "OM" and key != "csrfmiddlewaretoken"
        }

        if data["PayCustNum"]!="":
            data["PayCustNum"] = int(data["PayCustNum"][1:])
        if data["RcvCustNum"]!="":
            data["RcvCustNum"] = int(data["RcvCustNum"][1:])
        if data["DelDdl"]!="":
            time=str(data["DelDdl"])
            y=time.index("年")
            m=time.index("月")
            d=time.index("日")
            year=time[:y]
            month=time[y+1:m]
            day=time[m+1:d]
            data["DelDdl"] = datetime.datetime.strptime(year+"-"+month+"-"+day,"%Y-%m-%d")
        form1 = OrdSaveForm(data,instance=order)
        print(data)
        if form1.is_valid():
            form1.save()
            ordmat_qs.delete() #删了全部的
            for i in range(len(OM)):
                matnum = int(OM[i]["OM_MatNum"][1:])
                mat = Material.objects.get(pk=matnum)
                OrdMat.objects.create(
                    OM_OrdNum=order,
                    OM_MatNum=mat,
                    OrdMatDesc=OM[i]["OrdMatDesc"],
                    OrdMatQty=OM[i]["OrdMatQty"],
                    OdrMatDisc=OM[i]["OdrMatDisc"],
                )
            context.update(
                {
                    "is_suc": True,
                    "order": order,
                    "form1": OrdSaveForm(model_to_dict(order)),
                }
            )
        else:
            context.update(
                {
                    "is_error": True,
                    "error_msg": "格式有误",
                }
            )
    return render(request, "order/modify.html", context)


def detail(request, OrdNum):
    order = Order.objects.get(pk=OrdNum)
    ordmat_qs = OrdMat.objects.filter(OM_OrdNum=OrdNum)
    context = {"order": order, "ordmat_qs": ordmat_qs}
    return render(request, "order/detail.html", context)