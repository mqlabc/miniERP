from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from login.wrapper import login_required
from order.models import Order
from .generate_word import generate_word


# from django.views import generic

# Create your views here.
# class OrderList(generic.ListView):
#     paginate_by = 5
#     # 默认找material/order_list.html
#     template_name = 'order/index.html'
#
#     def get_queryset(self):
#         return Order.objects.all().order_by('-order_date')

@login_required
def listing(request):
    order_list = Order.objects.order_by('-order_date')
    paginator = Paginator(order_list, 5)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'order/index.html', {'page_obj': page_obj})


@login_required
def down_word(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    word_name = generate_word(order)
    f = open(f'word_files/{word_name}.docx', 'rb')
    return FileResponse(f, as_attachment=True, filename=f'{word_name}.docx')


# 没用上，不知道ajax拿到数据后怎么启用下载
def download(request):
    order_id = request.GET['order_id']
    order = get_object_or_404(Order, pk=order_id)

    word_name = generate_word(order)
    f = open(f'word_files/{word_name}.docx', 'rb')
    return FileResponse(f, as_attachment=True, filename=f'{word_name}.docx')
