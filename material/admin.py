from django.contrib import admin

from . import models


# Register your models here.
# 此处修改无需重新迁移数据库
class MaterialAdmin(admin.ModelAdmin):
    search_fields = ['material_name']
    list_display = ('material_name', 'material_spec', 'material_unit')


class MaterialRelationAdmin(admin.ModelAdmin):
    search_fields = ['mat']
    fields = ['mat', 'mat_pos', 'mat_parent', 'mat_num', 'mat_root']
    list_display = ('mat', 'mat_pos', 'mat_parent', 'mat_num', 'mat_root')




admin.site.register(models.Material, MaterialAdmin)
# admin.site.register(models.MaterialRelation, MaterialRelationAdmin)
