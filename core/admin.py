from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget

from .models import Categoria, Noticia, SocialLink, PortalConfig


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nome",)}
    search_fields = ("nome", "slug")
    list_display = ("nome", "order", "slug")
    list_editable = ("order",)
    ordering = ("order", "nome")


class NoticiaAdminForm(forms.ModelForm):
    conteudo = forms.CharField(
        required=True,
        widget=CKEditorWidget(config_name="default"),
        help_text="Conteúdo completo (aceita links, formatação).",
    )

    class Meta:
        model = Noticia
        fields = "__all__"


@admin.action(description="Marcar como Destaque principal")
def marcar_principal(modeladmin, request, queryset):
    queryset.update(destaque_principal=True)


@admin.action(description="Remover Destaque principal")
def remover_principal(modeladmin, request, queryset):
    queryset.update(destaque_principal=False)


@admin.action(description="Marcar como Destaque secundário")
def marcar_secundario(modeladmin, request, queryset):
    queryset.update(destaque_secundario=True)


@admin.action(description="Remover Destaque secundário")
def remover_secundario(modeladmin, request, queryset):
    queryset.update(destaque_secundario=False)


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    form = NoticiaAdminForm

    list_display = (
        "titulo",
        "categoria",
        "publicado",
        "destaque_principal",
        "destaque_secundario",
        "views_count",
        "publicado_em",
        "criado_em",
    )
    list_filter = ("categoria", "publicado", "destaque_principal", "destaque_secundario")
    search_fields = ("titulo", "resumo", "slug")
    prepopulated_fields = {"slug": ("titulo",)}
    date_hierarchy = "criado_em"
    ordering = ("-publicado_em", "-criado_em")
    actions = [marcar_principal, remover_principal, marcar_secundario, remover_secundario]


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ("platform", "is_visible", "order", "url")
    list_editable = ("is_visible", "order")
    search_fields = ("platform", "url")
    ordering = ("order", "platform")


class PortalConfigAdminForm(forms.ModelForm):
    # opcional: usar CKEditor “simples” no texto do rodapé
    about_text = forms.CharField(
        required=False,
        widget=CKEditorWidget(config_name="summary"),
        help_text="Texto do 'Sobre o portal' no rodapé.",
    )
    about_text_muted = forms.CharField(
        required=False,
        widget=CKEditorWidget(config_name="summary"),
        help_text="Linha menor abaixo do texto principal.",
    )

    class Meta:
        model = PortalConfig
        fields = "__all__"


@admin.register(PortalConfig)
class PortalConfigAdmin(admin.ModelAdmin):
    form = PortalConfigAdminForm

    fieldsets = (
        ("Identidade", {"fields": ("about_name", "about_tagline")}),
        ("Texto do rodapé", {"fields": ("about_text", "about_text_muted")}),
        ("Linha de copyright", {"fields": ("copyright_text",)}),
    )

    def has_add_permission(self, request):
        # força singleton: só deixa criar se ainda não existir nenhum
        return not PortalConfig.objects.exists()
