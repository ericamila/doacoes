from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from payment.forms import PaymentForm
from payment.models import Payment


# Create your views here.
def lists(request):
    payments_list = Payment.objects.filter(removido_em=None)
    obj = request.GET.get("obj")  # Implementa o mecanismo de busca

    if obj:
        payments_list = payments_list.filter(codigo__icontains=obj) | payments_list.filter(
            situacao__icontains=obj)

    else:
        payments_list = payments_list.order_by('-data', 'codigo')

    paginator = Paginator(payments_list, 10)  # Define 10 itens fixos por página
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    return render(request, "payment/list.html",
                  {
                      "payments": page_obj,
                      "page_obj": page_obj,
                  }
                  )


def detail(request, id):
    payment = get_object_or_404(Payment, pk=id)
    form = PaymentForm(instance=payment)
    return render(request, "payment/detail.html",
                  {
                      "payment": payment,
                      "form": form,
                  }
                  )
