import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Timeline
from pyecharts.globals import ThemeType
from login.wrapper import login_required
from .models import Debt


# from pyecharts.globals import CurrentConfig
# 不管用？采用模拟模板加载js的方式，看看模板中的js被解析成了什么，在embedded中替换
# CurrentConfig.ONLINE_HOST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'static\echarts.min.js')

# Create your views here.

@login_required
def index(request):
    debts = Debt.objects.filter(Q(clear=False) & Q(order__seller__id=1))
    all_debts_sum = sum((i.order.get_sum() for i in debts))
    return render(request, 'debt/table.html', {'debts': debts, 'all_debts_sum': all_debts_sum})

@login_required
def overdue(request):
    debts = Debt.objects.filter(Q(clear=False) & Q(order__seller__id=1) & Q(last_date__lt=datetime.datetime.now()))
    all_debts_sum = sum((i.order.get_sum() for i in debts))
    return render(request, 'debt/overdue.html', {'debts': debts, 'all_debts_sum': all_debts_sum})


def change_order_status(request):
    # 错误
    # debt_id=request.GET('debt_id')
    debt_id = request.GET['debt_id']
    # id不是一般的属性只有一个 _
    # debts=Debt.objects.get(order_id=order_id)
    debt = Debt.objects.get(id=debt_id)
    if not debt.clear:
        debt.clear = True
    else:
        debt.clear = False
    debt.save()
    return HttpResponse(debt.clear)


def get_comps_sum(df):
    """docstring for get_comps_sum"""
    months = df['order_date'].max().month - df['order_date'].min().month + 1
    comps = ['泰山集团股份有限公司', '泰安市金智达机器人科技有限责任公司', '普瑞特机械制造股份有限公司', '山东泰开高压开关有限公司', '泰安华鲁锻压机床有限公司']
    by = df.groupby('comp_name')
    d = {}
    for comp in comps:
        if comp not in by.groups:
            d[comp]=[0]*months
            continue
        new_df = by.get_group(comp)
        new_df.set_index('order_date', inplace=True)
        need2pad = new_df.resample('M')['sum'].sum().to_list()
        if len(need2pad) < months:
            # extend无返回值
            need2pad.extend([0] * (months - len(need2pad)))
        d[comp] = need2pad
    return d


def gen_chart(df):
    start = df['order_date'].min()
    end = df['order_date'].max() + relativedelta(months=1)
    r = pd.date_range(start, end, freq='M').to_list()
    time_range = [i.strftime('%Y-%m') for i in r]

    result = get_comps_sum(df)
    c = (
        Bar(init_opts=opts.InitOpts(width="500px", height="600px", theme=ThemeType.SHINE))
            .add_xaxis(time_range)
            .add_yaxis("泰山集团股份有限公司", result['泰山集团股份有限公司'], stack='stack1')
            .add_yaxis("泰安市金智达机器人科技有限责任公司", result['泰安市金智达机器人科技有限责任公司'], stack='stack1')
            .add_yaxis("普瑞特机械制造股份有限公司", result['普瑞特机械制造股份有限公司'], stack='stack1')
            .add_yaxis("山东泰开高压开关有限公司", result['山东泰开高压开关有限公司'], stack='stack1')
            .add_yaxis("泰安华鲁锻压机床有限公司", result['泰安华鲁锻压机床有限公司'], stack='stack1')
            # 去掉bar顶端数字
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(formatter='{a}<br>在{b}月份欠款:<br>{c}元'),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )

    time_line = Timeline(init_opts=opts.InitOpts(width="1000px", height="500px", theme=ThemeType.SHINE))
    comps = ['泰山集团股份有限公司', '泰安市金智达机器人科技有限责任公司', '普瑞特机械制造股份有限公司', '山东泰开高压开关有限公司', '泰安华鲁锻压机床有限公司']
    for i, d in enumerate(time_range):
        pie = Pie(init_opts=opts.InitOpts(width="800px", height="800px", theme=ThemeType.SHINE))
        pie.add('', [[comp, result[comp][i]] for comp in comps])
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        pie.set_global_opts(tooltip_opts=opts.TooltipOpts(formatter='{a}<br>在{b}月份欠款:<br>{c}元'), )
        time_line.add(pie, d)

    return c, time_line


def gen_chart_(df):
    df0 = df.loc[df['clear'] == False]

    start = df['order_date'].min()
    end = df['order_date'].max() + relativedelta(months=1)
    r = pd.date_range(start, end, freq='M').to_list()
    time_range = [i.strftime('%Y-%m') for i in r]

    result = get_comps_sum(df)
    result0 = get_comps_sum(df0)

    c = (
        Bar(init_opts=opts.InitOpts(width="1000px", height="600px", theme=ThemeType.SHINE))
            .add_xaxis(time_range)
            .add_yaxis("泰山集团股份有限公司", result['泰山集团股份有限公司'], stack='stack1')
            .add_yaxis("泰山集团股份有限公司", result0['泰山集团股份有限公司'], stack='stack0')
            .add_yaxis("泰安市金智达机器人科技有限责任公司", result['泰安市金智达机器人科技有限责任公司'], stack='stack1')
            .add_yaxis("泰安市金智达机器人科技有限责任公司", result0['泰安市金智达机器人科技有限责任公司'], stack='stack0')
            .add_yaxis("普瑞特机械制造股份有限公司", result['普瑞特机械制造股份有限公司'], stack='stack1')
            .add_yaxis("普瑞特机械制造股份有限公司", result0['普瑞特机械制造股份有限公司'], stack='stack0')
            .add_yaxis("山东泰开高压开关有限公司", result['山东泰开高压开关有限公司'], stack='stack1')
            .add_yaxis("山东泰开高压开关有限公司", result0['山东泰开高压开关有限公司'], stack='stack0')
            .add_yaxis("泰安华鲁锻压机床有限公司", result['泰安华鲁锻压机床有限公司'], stack='stack1')
            .add_yaxis("泰安华鲁锻压机床有限公司", result0['泰安华鲁锻压机床有限公司'], stack='stack0')
            # 去掉bar顶端数字
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            tooltip_opts=opts.TooltipOpts(formatter='{a}<br>在{b}月份:<br>{c}元'),
            datazoom_opts=[opts.DataZoomOpts(), opts.DataZoomOpts(type_="inside")],
        )
    )

    time_line = Timeline(init_opts=opts.InitOpts(width="1000px", height="500px", theme=ThemeType.SHINE))
    comps = ['泰山集团股份有限公司', '泰安市金智达机器人科技有限责任公司', '普瑞特机械制造股份有限公司', '山东泰开高压开关有限公司', '泰安华鲁锻压机床有限公司']
    for i, d in enumerate(time_range):
        pie = Pie(init_opts=opts.InitOpts(width="800px", height="800px", theme=ThemeType.SHINE))
        pie.add('', [[comp, result0[comp][i]] for comp in comps])
        pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
        pie.set_global_opts(tooltip_opts=opts.TooltipOpts(formatter='{b}<br>欠款:<br>{c}元'), )
        time_line.add(pie, d)

    pie = (
        Pie(init_opts=opts.InitOpts(width="1000px", height="500px", theme=ThemeType.SHINE))
            .add('', [[comp, sum(result0[comp])] for comp in comps])
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
            .set_global_opts(tooltip_opts=opts.TooltipOpts(formatter='{b}<br>欠款:<br>{c}元'), )
    )

    return c, time_line, pie

@login_required
def charts(request):
    # 考虑自己为乙方
    debts = Debt.objects.filter(order__seller__id=1)
    df = pd.DataFrame({'comp_name': [debt.order.buyer.comp_name for debt in debts],
                       'order_date': [debt.order.order_date for debt in debts],
                       'sum': [debt.order.get_sum() for debt in debts],
                       'last_date': [debt.last_date for debt in debts],
                       'clear': [debt.clear for debt in debts]})
    df['order_date'] = pd.to_datetime(df['order_date'])
    # df0 = df.loc[df['clear'] == False]
    #     #
    #     # c=gen_chart(df)[0]
    #     # time_line=gen_chart(df)[1]
    c0 = gen_chart_(df)[0]
    time_line0 = gen_chart_(df)[1]
    pie = gen_chart_(df)[2]

    return render(request, 'debt/test.html', {
        # 'bar': c.render_embed(),
        'bar0': c0.render_embed().replace('https://assets.pyecharts.org/assets/echarts.min.js',"/static/echarts.min.js").replace('https://assets.pyecharts.org/assets/themes/shine.js',"/static/shine.js"),
        'time_line': time_line0.render_embed().replace('https://assets.pyecharts.org/assets/echarts.min.js',"/static/echarts.min.js").replace('https://assets.pyecharts.org/assets/themes/shine.js',"/static/shine.js"),
        'pie': pie.render_embed().replace('https://assets.pyecharts.org/assets/echarts.min.js',"/static/echarts.min.js").replace('https://assets.pyecharts.org/assets/themes/shine.js',"/static/shine.js"),
    })
