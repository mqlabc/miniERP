from django.db import models


# Create your models here.
class Material(models.Model):
    material_name = models.CharField(max_length=200, verbose_name='产品名称')
    material_spec = models.CharField(max_length=100, verbose_name='产品规格')
    # material_type = models.CharField(max_length=100, verbose_name='产品类型（采购产品、中间产品、最终产品）')
    material_unit = models.CharField(max_length=10, verbose_name='产品单位')
    material_num = models.IntegerField(verbose_name='数量')
    material_price = models.FloatField(verbose_name='单价')
    material_date = models.DateField(verbose_name='交货日期')
    material_expl = models.CharField(max_length=200, verbose_name='备注')

    def __str__(self):
        return self.material_name +' 规格：'+ self.material_spec + f' 单价：{self.material_price}元'

    class Meta:
        verbose_name = "产品"
        verbose_name_plural = "产品"


class MaterialRelation(models.Model):
    mat = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='产品', related_name='mat_mat')
    mat_root = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='最终产品', related_name='root_mat')
    mat_parent = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='上层产品', related_name='parent_mat')
    mat_pos = models.SmallIntegerField(verbose_name='产品层次')
    mat_num = models.IntegerField(verbose_name='组成上层产品的数量')

    def get_parent(self, parent):
        return Material.objects.get(material_name=parent.material_name)

    def __str__(self):
        unit = self.get_parent(self.mat_parent).material_unit
        return str(self.mat_num) + unit + str(self.mat)

    class Meta:
        verbose_name = "产品关系"
        verbose_name_plural = "产品关系"


