from .models import SocialLink, PortalConfig


def social_links(request):
    links = (
        SocialLink.objects
        .filter(is_visible=True)
        .exclude(url="")
        .order_by("order", "platform")
    )

    # ✅ config do portal (singleton)
    try:
        config = PortalConfig.get_solo()
    except Exception:
        # se ainda não migrou, evita quebrar o site
        config = None

    return {"SOCIAL_LINKS": links, "PORTAL_CONFIG": config}
