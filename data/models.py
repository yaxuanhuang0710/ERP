from django.db import models

FEATURE_CODE = {
    "Lang": (
        ("EN", "英语"),
        ("ZH", "汉语"),
        ("ES", "西班牙语"),
        ("FR", "法语"),
        ("PT", "葡萄牙语"),
        ("DE", "德语"),
    ),
    "Div": (
        ("BI", "自行车"),
        ("AS", "配件"),
        ("00", "自行车&配件"),
        ("01", "其他"),
    ),
    "Cur": (
        ("CNY", "人民币"),
        ("HKD", "港元"),
        ("TWD", "台币"),
        ("EUR", "欧元"),
        ("USD", "美元"),
        ("GBP", "英镑"),
        ("JPY", "日元"),
    ),
}


class Material(models.Model):
    MatNum = models.AutoField(primary_key=True)
    MatName = models.CharField(max_length=50)
    Weight = models.DecimalField(decimal_places=5, max_digits=10)
    MatDesc = models.CharField(max_length=50)
    Price = models.DecimalField(decimal_places=5, max_digits=10)

    def __str__(self) -> str:
        return "M{:0>4d}".format(self.MatNum)


class Plant(models.Model):
    PlantNum = models.AutoField(primary_key=True)
    PlantName = models.CharField(max_length=50)
    PlantLoc = models.CharField(max_length=50)
    materials = models.ManyToManyField(Material, through="PlantMat")

    def __str__(self) -> str:
        return "P{:0>4d}".format(self.PlantNum)


class PlantMat(models.Model):
    PM_PlantNum = models.ForeignKey(Plant, on_delete=models.CASCADE)
    PM_MatNum = models.ForeignKey(Material, on_delete=models.CASCADE)
    Stock = models.IntegerField()


class Customer(models.Model):
    CustNum = models.AutoField(primary_key=True)
    CustName = models.CharField(max_length=50)
    CustAddr = models.CharField(max_length=50)
    Lang = models.CharField(choices=FEATURE_CODE["Lang"], max_length=3, default="ZH")
    Div = models.CharField(choices=FEATURE_CODE["Div"], max_length=3, default="BI")
    CustCur = models.CharField(choices=FEATURE_CODE["Cur"], max_length=3, default="CNY")
    SearchTerm = models.CharField(max_length=5)
    DelPlant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "C{:0>4d}".format(self.CustNum)


class Order(models.Model):
    OrdNum = models.AutoField(primary_key=True)
    PayCustNum = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="PayCustNum"
    )
    RcvCustNum = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="RcvCustNum"
    )
    OrdCur = models.CharField(choices=FEATURE_CODE["Cur"], max_length=3, default="CNY")
    OdrCreDate = models.DateField(auto_now=False, auto_now_add=True)
    DelDdl = models.DateField(auto_now=False, auto_now_add=False)
    IsPost = models.BooleanField(default=False)
    TotDisc = models.DecimalField(decimal_places=5, max_digits=5)
    materials = models.ManyToManyField(Material, through="OrdMat")

    def __str__(self) -> str:
        return "1{:0>8d}".format(self.OrdNum)


class OrdMat(models.Model):
    OM_OrdNum = models.ForeignKey(Order, on_delete=models.CASCADE)
    OM_MatNum = models.ForeignKey(Material, on_delete=models.CASCADE)
    OrdMatDesc = models.CharField(max_length=50)
    OrdMatQty = models.IntegerField()
    OdrMatDisc = models.DecimalField(decimal_places=5, max_digits=10)


class Delivery(models.Model):
    DelNum = models.AutoField(primary_key=True)
    DelOrdNum = models.OneToOneField(Order, on_delete=models.CASCADE)
    DelCreDate = models.DateField(auto_now=False, auto_now_add=True)
    PostDdl = models.DateField(auto_now=False, auto_now_add=False)
    PostDate = models.DateField(auto_now=False, auto_now_add=False, null=True,blank=True)

    def __str__(self) -> str:
        return "2{:0>8d}".format(self.DelNum)


class User(models.Model):
    username = models.CharField(max_length=5, primary_key=True)
    password = models.CharField(max_length=20)
