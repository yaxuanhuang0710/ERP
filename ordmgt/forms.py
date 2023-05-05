from django import forms
from data.models import *


class OrdSaveForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ("materials",)
        labels = {
            "PayCustNum": "付款客户号",
            "RcvCustNum": "收货账户号",
            "OrdCur": "货币",
            "OdrCreDate": "创建日期",
            "IsPost": "是否创建发货单",
            "DelDdl": "发货单截止日期",
            "TotDisc": "总折扣（）",
        }


class OrdMatSaveForm(forms.ModelForm):
    class Meta:
        model = OrdMat
        exclude = ("OM_OrdNum",)
        labels = {
            "OM_MatNum": "物料号",
            "OrdMatDesc": "材料描述",
            "OrdMatQty": "数量",
            "OdrMatDisc": "折扣",
        }


class OrdInqueryForm(forms.Form):
    OrdNum = forms.CharField(required=False, label="订单号")
    PayCustNum = forms.CharField(required=False, label="付款客户号")
    RcvCustNum = forms.CharField(required=False, label="收货账户号")
    OrdCur = forms.ChoiceField(
        choices=FEATURE_CODE["Cur"] + (("", "---------"),), required=False, label="货币"
    )
    OdrCreDate = forms.DateField(required=False, label="创建日期")
    DelDdl = forms.DateField(required=False, label="发货单截止日期")
    IsPost = forms.IntegerField(required=False, label="是否创建发货单")
    TotDisc = forms.DecimalField(required=False, label="折扣")


class OrdMatInqueryForm(forms.Form):
    OM_OrdNum=forms.CharField(required=False, label="订单号")
    OM_MatNum = forms.CharField(required=False, label="材料号")
    OrdMatDesc = forms.CharField(required=False, label="材料描述")
    OrdMatQty = forms.DateField(required=False, label="材料数量")
    OdrMatDisc = forms.DateField(required=False, label="材料折扣")
