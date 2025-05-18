from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from proposals.models import Proposal
from projects.forms import ProjectForm
from .models import Project
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages


def lists(request):
    projects_list = Project.objects.filter(removido_em=None)
    obj = request.GET.get("obj")  # Implementa o mecanismo de busca

    if obj:
        projects_list = projects_list.filter(removido_em=None, orgao_repassador__icontains=obj)
    else:
        projects_list = projects_list.order_by('-ano', 'codigo')

    paginator = Paginator(projects_list, 10)  # Define 10 itens fixos por página
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    return render(
        request,
        "projects/list.html",
        {
            "projects": page_obj,
            "page_obj": page_obj,
        },
    )


# Leitura de Projects
def detail(request, id):
    project = get_object_or_404(Project, pk=id)
    form = ProjectForm(instance=project)

    # Emendas vinculadas ao project
    proposals = Proposal.objects.filter(removido_em=None, project=project)

    return render(
        request,
        "projects/detail.html",
        {
            "project": form,
            'proposals': proposals,
        },
    )


# Criação de Project
def new(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Project enviado com sucesso!")
            return redirect("new")
        else:
            messages.error(request, "Erro ao salvar o project. Verifique os campos.")
    else:
        form = ProjectForm()

    return render(request, "projects/new.html", {"project_form": form})


def edit(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            messages.success(request, "Project atualizado com sucesso!")
        else:
            messages.error(request, "Erro ao salvar o project. Verifique os campos.")

    else:
        form = ProjectForm(instance=project)

    return render(request, "projects/edit.html", {"form": form, "project": project})


# Remoção de Project
def remove(request, id):
    project = get_object_or_404(Project, pk=id)

    if request.method == "POST":
        project.removido_em = datetime.now()
        project.save()

        # Excluir proposals vinculadas ao project
        proposals = Proposal.objects.filter(project=project)
        for proposal in proposals:
            proposal.removido_em = datetime.now()
            proposal.save()

    return redirect("projects:list")
