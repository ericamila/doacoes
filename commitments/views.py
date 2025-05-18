from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from commitments.forms import CommitmentForm
from commitments.models import Commitment


# Create your views here.
def lists(request):
    commitments_list = Commitment.objects.filter(removido_em=None)
    obj = request.GET.get("obj")  # Implementa o mecanismo de busca

    if obj:
        commitments_list = commitments_list.filter(codigo__icontains=obj) | commitments_list.filter(situacao__icontains=obj)
    else:
        commitments_list = commitments_list.order_by('-data', 'codigo')

    paginator = Paginator(commitments_list, 10)  # Define 10 itens fixos por página
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    return render(request, "commitments/list.html",
                  {
                      "commitments": page_obj,
                      "page_obj": page_obj,
                  }
                  )


def detail(request, id):
    commitment = get_object_or_404(Commitment, pk=id)
    form = CommitmentForm(instance=commitment)
    return render(request, "commitments/detail.html",
                  {
                      "commitment": commitment,
                      "form": form,
                  }
                  )
