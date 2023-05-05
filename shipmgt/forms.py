from data.models import *
from django import forms


class DelSaveForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields =  ["DelOrdNum","PostDdl"]
        labels = {
            "DelOrdNum": "订单号",
            "PostDdl": "发货截止日期",
        }


class DelModifyForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ["PostDdl"]
        labels = {
            "PostDdl": "发货截止日期",
        }


class PostForm(forms.Form):
    DelNum = forms.CharField(max_length=50, required=True, label="发货单号")


class DelInqueryForm(forms.Form):
    DelNum = forms.CharField(max_length=50, required=False, label="发货单号")
    DelOrdNum = forms.CharField(max_length=50, required=False, label="订单号")
    DelCreDate = forms.DateField(required=False, label="创建日期")
    PostDdl = forms.DateField(required=False, label="发货截止日期")
    PostDate = forms.DateField(required=False, label="发货日期")


class CheckStockForm(forms.Form):
    MatNum = forms.CharField(max_length=50, required=False, label="物料号")
    MatName = forms.DateField(required=False, label="物料名称")
    MatDesc = forms.DateField(required=False, label="物料描述")
