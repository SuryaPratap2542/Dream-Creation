from .models import Cart
# this function is used for show the no of cart item on each page
# here vews then add it settings template and then base.html
def cart_count(request):
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_count = 0
    return {'cart_count': cart_count}
