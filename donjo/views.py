from django.shortcuts import render
from django.shortcuts import redirect


def index(request):
    # if not request.user.is_authenticated:
    #     return redirect('users:login')

    # products = Product.objects.all().order_by('-id')

    return render(request, 'index.html', {
        'head_title': 'Productos',
        'body_title': 'Listado de productos',
        # 'products': products
    })
