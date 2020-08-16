from django.core.paginator import Paginator
from django.shortcuts import render
from login.wrapper import login_required

from .models import Material

@login_required
def listing(request):
    material_list = Material.objects.order_by('material_date')
    big_sum = sum((i.material_price * i.material_num) for i in material_list)
    paginator = Paginator(material_list, 5)  # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'material/material_list.html', {'page_obj': page_obj, 'big_sum': big_sum})
