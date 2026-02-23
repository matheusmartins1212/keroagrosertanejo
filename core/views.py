from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F

from .models import Categoria, Noticia


def home(request):
    categorias = Categoria.objects.all().order_by("order", "nome")

    cat = request.GET.get("cat")
    noticias_qs = Noticia.objects.filter(publicado=True)

    if cat:
        noticias_qs = noticias_qs.filter(categoria__slug=cat)

    destaque_principal = (
        noticias_qs.filter(destaque_principal=True)
        .order_by("-publicado_em", "-criado_em")
        .first()
    )

    # ✅ não limita mais a 3 (mantido 12 pra ficar leve e evitar lista infinita)
    destaques_menores = (
        noticias_qs.filter(destaque_secundario=True)
        .exclude(pk=getattr(destaque_principal, "pk", None))
        .order_by("-publicado_em", "-criado_em")[:12]
    )

    ultimas_publicacoes = noticias_qs.order_by("-publicado_em", "-criado_em")[:8]

    mais_lidas = noticias_qs.order_by("-views_count", "-publicado_em", "-criado_em")[:6]

    return render(
        request,
        "core/home.html",
        {
            "categorias": categorias,
            "cat_ativa": cat,
            "destaque_principal": destaque_principal,
            "destaques_menores": destaques_menores,
            "ultimas_publicacoes": ultimas_publicacoes,
            "mais_lidas": mais_lidas,
        },
    )


def noticia_detalhe(request, slug):
    categorias = Categoria.objects.all().order_by("order", "nome")

    noticia = get_object_or_404(Noticia, slug=slug, publicado=True)

    # incrementa visualizações
    Noticia.objects.filter(pk=noticia.pk).update(views_count=F("views_count") + 1)
    noticia.views_count += 1

    relacionadas = (
        Noticia.objects.filter(publicado=True, categoria=noticia.categoria)
        .exclude(id=noticia.id)
        .order_by("-publicado_em", "-criado_em")[:6]
    )

    return render(
        request,
        "core/noticia.html",
        {
            "categorias": categorias,
            "noticia": noticia,
            "relacionadas": relacionadas,
        },
    )


def buscar(request):
    categorias = Categoria.objects.all().order_by("order", "nome")

    q = (request.GET.get("q") or "").strip()
    noticias = Noticia.objects.filter(publicado=True)

    if q:
        noticias = noticias.filter(
            Q(titulo__icontains=q)
            | Q(resumo__icontains=q)
            | Q(conteudo__icontains=q)
        ).order_by("-publicado_em", "-criado_em")
    else:
        noticias = Noticia.objects.none()

    return render(
        request,
        "core/buscar.html",
        {
            "categorias": categorias,
            "q": q,
            "noticias": noticias,
        },
    )
