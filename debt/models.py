from django.db import models

from order.models import Order


# Create your models here.
class Debt(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    # 在sqlite种用0和1表示，造数据时需要注意
    clear = models.BooleanField(default=False, verbose_name='是否全部回款')

    alredy_cleared=models.FloatField(default=0, verbose_name='已收款金额')
    last_date = models.DateField(verbose_name='应收日期')

    def __str__(self):
        return f'{self.order.order_date} {self.order.buyer} 欠 {self.order.get_sum()}元'



    class Meta:
        verbose_name = "应收账款"
        verbose_name_plural = "应收账款"