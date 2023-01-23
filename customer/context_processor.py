from api.models import carts


def cart_count(request):
    if request.user.is_authenticated:
        count=carts.objects.filter(user=request.user).count()
    else:
        count=0
    return {"count":count} 