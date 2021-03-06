# Generated by Django 2.2 on 2020-08-04 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Debt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clear', models.BooleanField(default=False, verbose_name='已付款')),
                ('last_date', models.DateField(verbose_name='应付日期')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order', verbose_name='订单')),
            ],
            options={
                'verbose_name': '应付账款',
                'verbose_name_plural': '应付账款',
            },
        ),
    ]
