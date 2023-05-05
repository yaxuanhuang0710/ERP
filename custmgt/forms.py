from django import forms
from data.models import *


class CustSaveForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        labels = {
            "CustName": "客户名",
            "CustAddr": "地址",
            "Lang": "语言",
            "Div": "部门",
            "CustCur": "货币",
            "SearchTerm": "搜索项",
            "DelPlant": "交货工厂",
        }


class CustInqueryForm(forms.Form):
    CustNum = forms.CharField(max_length=50, required=False, label="客户号")
    CustName = forms.CharField(max_length=50, required=False, label="客户名")
    CustAddr = forms.CharField(max_length=50, required=False, label="地址")
    Lang = forms.ChoiceField(
        choices=FEATURE_CODE["Lang"] + (("", "---------"),), required=False, label="语言"
    )
    Div = forms.ChoiceField(
        choices=FEATURE_CODE["Div"] + (("", "---------"),), required=False, label="部门"
    )
    CustCur = forms.ChoiceField(
        choices=FEATURE_CODE["Cur"] + (("", "---------"),), required=False, label="货币"
    )
    SearchTerm = forms.CharField(max_length=5, required=False, label="搜索项")
    DelPlant = forms.ModelChoiceField(Plant.objects.all(), required=False, label="交货工厂")
