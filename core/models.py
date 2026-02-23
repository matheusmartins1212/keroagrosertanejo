from __future__ import annotations

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Categoria(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    order = models.PositiveIntegerField("Ordem", default=0)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["order", "nome"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nome) or "categoria"
            slug = base
            i = 2
            while Categoria.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    resumo = models.TextField(max_length=300, blank=True)
    conteudo = models.TextField()

    imagem = models.ImageField(upload_to="noticias/", blank=True, null=True)

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="noticias",
    )

    publicado = models.BooleanField(default=False)

    destaque_principal = models.BooleanField("Destaque principal", default=False)
    destaque_secundario = models.BooleanField("Destaque secundário", default=False)

    views_count = models.PositiveIntegerField("Visualizações", default=0, editable=False)

    criado_em = models.DateTimeField(auto_now_add=True)
    publicado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Notícia"
        verbose_name_plural = "Notícias"
        ordering = ["-publicado_em", "-criado_em"]
        indexes = [
            models.Index(fields=["publicado", "-publicado_em"]),
            models.Index(fields=["destaque_principal", "publicado", "-publicado_em"]),
            models.Index(fields=["destaque_secundario", "publicado", "-publicado_em"]),
            models.Index(fields=["views_count"]),
            models.Index(fields=["slug"]),
        ]

    def _generate_unique_slug(self) -> str:
        base = slugify(self.titulo) or "noticia"
        slug = base
        i = 2
        while Noticia.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._generate_unique_slug()

        if self.publicado:
            if not self.publicado_em:
                self.publicado_em = timezone.now()

            # ✅ se marcou como principal, não faz sentido ser secundário também
            if self.destaque_principal:
                self.destaque_secundario = False

        else:
            self.publicado_em = None
            self.destaque_principal = False
            self.destaque_secundario = False

        super().save(*args, **kwargs)

        # ✅ garante só 1 destaque principal no site
        if self.publicado and self.destaque_principal:
            Noticia.objects.filter(destaque_principal=True).exclude(pk=self.pk).update(
                destaque_principal=False
            )

    def __str__(self):
        return self.titulo


class SocialLink(models.Model):
    PLATFORM_INSTAGRAM = "instagram"
    PLATFORM_YOUTUBE = "youtube"
    PLATFORM_X = "x"
    PLATFORM_FACEBOOK = "facebook"
    PLATFORM_WHATSAPP = "whatsapp"

    PLATFORM_CHOICES = [
        (PLATFORM_INSTAGRAM, "Instagram"),
        (PLATFORM_YOUTUBE, "YouTube"),
        (PLATFORM_X, "X (Twitter)"),
        (PLATFORM_FACEBOOK, "Facebook"),
        (PLATFORM_WHATSAPP, "WhatsApp"),
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, unique=True)
    url = models.URLField("Link", blank=True)
    is_visible = models.BooleanField("Visível no topo", default=False)
    order = models.PositiveIntegerField("Ordem", default=0)

    class Meta:
        ordering = ["order", "platform"]
        verbose_name = "Rede social"
        verbose_name_plural = "Redes sociais"

    def __str__(self) -> str:
        return dict(self.PLATFORM_CHOICES).get(self.platform, self.platform)


class PortalConfig(models.Model):
    """
    Configurações gerais do portal (rodapé).
    A ideia é ter apenas 1 registro (singleton).
    """
    about_name = models.CharField("Nome do portal", max_length=80, default="Kero Agro")
    about_tagline = models.CharField(
        "Slogan/descrição curta",
        max_length=120,
        default="Portal de notícias do agro e sertanejo",
        blank=True,
    )

    about_text = models.TextField(
        "Texto principal (Sobre o portal)",
        blank=True,
        default=(
            "O Kero Agro é um portal de conteúdo sobre agricultura, pecuária, "
            "agronegócio e cultura sertaneja. Informação com linguagem simples, "
            "visual limpo e foco no que importa no campo."
        ),
    )
    about_text_muted = models.TextField(
        "Texto secundário (linha menor)",
        blank=True,
        default="Produzimos conteúdo com responsabilidade e independência editorial.",
    )

    copyright_text = models.CharField(
        "Texto de copyright",
        max_length=140,
        blank=True,
        default="© 2026 Kero Agro — Portal de notícias do agro.",
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuração do portal"
        verbose_name_plural = "Configurações do portal"

    def __str__(self) -> str:
        return "Configuração do portal"

    @classmethod
    def get_solo(cls) -> "PortalConfig":
        obj = cls.objects.order_by("id").first()
        if obj:
            return obj
        return cls.objects.create()
