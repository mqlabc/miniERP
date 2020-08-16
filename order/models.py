from django.db import models
from material.models import Material

# Create your models here.
class Company(models.Model):
    comp_name = models.CharField(max_length=200, verbose_name='公司名称')
    comp_addr = models.CharField(max_length=200, verbose_name='公司地址',blank=True)
    comp_legal_person = models.CharField(max_length=100, verbose_name='法定代表人',blank=True)
    comp_agent_person = models.CharField(max_length=100, verbose_name='委托代理人',blank=True)
    comp_phone = models.CharField(max_length=20, verbose_name='电话',blank=True)
    comp_mail = models.CharField(max_length=20, verbose_name='邮编',blank=True)
    comp_bank_name = models.CharField(max_length=30, verbose_name='开户银行',blank=True)
    comp_bank_account = models.CharField(max_length=30, verbose_name='银行账号',blank=True)
    comp_tax_account = models.CharField(max_length=30, verbose_name='税号',blank=True)
    comp_contact_person = models.CharField(max_length=30, verbose_name='联系人',blank=True)

    def __str__(self):
        return self.comp_name

    class Meta:
        verbose_name = "客户"
        verbose_name_plural = "客户"


class Order(models.Model):
    buyer = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comp_buyer', verbose_name='甲方')
    seller = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='comp_seller', verbose_name='乙方')
    mat_set = models.ManyToManyField(Material, related_name='mat_order', verbose_name='产品列表')
    order_place = models.CharField(max_length=200, verbose_name='合同签订地点')
    order_code = models.CharField(max_length=200, verbose_name='甲方合同编号')
    order_date = models.DateField(verbose_name='合同签订日期')
    deposit_percent = models.FloatField(verbose_name='预付定金比例（百分数）',default=0.0)

    def __str__(self):
        return self.order_code

    def get_sum(self):
        return sum((mat.material_price*mat.material_num for mat in self.mat_set.all()))

    def get_deposit(self):
        return sum((mat.material_price*mat.material_num for mat in self.mat_set.all()))*self.deposit_percent/100

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = "订单"