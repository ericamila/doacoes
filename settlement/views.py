from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from settlement.forms import SettlementForm
from settlement.models import Settlement

# Create your views here.
def lists(request):
    settlements_list = Settlement.objects.filter(removido_em=None)
    obj = request.GET.get("obj")  # Implementa o mecanismo de busca

    if obj:
        settlements_list = settlements_list.filter(codigo__icontains=obj) | settlements_list.filter(situacao__icontains=obj) 
    else:
        settlements_list = settlements_list.order_by('-data', 'codigo')

    paginator = Paginator(settlements_list, 10)  # Define 10 itens fixos por página
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    return render(request, "settlement/list.html",
        {
            "settlements": page_obj,
            "page_obj": page_obj,
        }
    )


def detail(request, id):
    settlement = get_object_or_404(Settlement, pk=id)
    form = SettlementForm(instance=settlement)
    return render(request, "settlement/detail.html", 
        {
            "settlement": settlement,
            "form": form,
        }
    )
