from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm
from .models import Category, Product, OrderItem
from .services.novaposhta import get_cities, get_warehouses


def home(request):
    return render(request, 'store/landing/home.html')


def about(request):
    return render(request, 'store/landing/about.html')


def aromadiagnostics(request):
    return render(request, 'store/landing/aromadiagnostics.html')


def product_list(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category_slug = request.GET.get('category')
    query = request.GET.get('q', '')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'store/catalog/product_list.html',
        {
            'categories': categories,
            'page_obj': page_obj,
            'query': query,
            'current_category': category_slug,
        }
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product,
        slug=slug,
        available=True
    )

    form = CartAddProductForm()

    return render(
        request,
        'store/catalog/product_detail.html',
        {
            'product': product,
            'form': form
        }
    )


def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override') == 'True'

    cart.add(
        product=product,
        quantity=quantity,
        override_quantity=override
    )

    # AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            "success": True,
            "cart_count": len(cart),
            "cart_total": float(cart.get_total_price()),
            "product_id": product.id,
        })

    # fallback
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))


def cart_remove(request, product_id):
    if request.method != 'POST':
        return redirect('store:cart_detail')

    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            "success": True,
            "cart_count": len(cart),
            "cart_total": float(cart.get_total_price()),
        })

    return redirect('store:cart_detail')


def cart_detail(request):
    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={
                'quantity': item['quantity'],
                'override': True
            }
        )

    return render(
        request, 'store/cart/cart_detail.html', {'cart': cart})


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity']
                )

            request.session['cart'] = {}

            return render(request, 'store/order/order_created.html', {'order': order})
    else:
        initial_data = {}

        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }

        form = OrderCreateForm(initial=initial_data)

    return render(request, 'store/order/order_create.html', {'cart': cart, 'form': form})


def api_cities(request):
    query = request.GET.get("q", "")

    if not query:
        return JsonResponse({"results": []})

    cities = get_cities(query)
    return JsonResponse({"results": cities})


def api_warehouses(request):
    city_ref = request.GET.get("city_ref")

    if not city_ref:
        return JsonResponse({"results": []})

    warehouses = get_warehouses(city_ref)
    return JsonResponse({"results": warehouses})


def privacy_policy(request):
    return render(request, 'store/privacy/privacy.html')