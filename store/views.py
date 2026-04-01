from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from .forms import CartAddProductForm, OrderCreateForm
from .models import Category, Product, OrderItem


def home(request):
    return render(request, 'store/home.html')


def about(request):
    return render(request, 'store/about.html')


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
        'store/product_list.html',
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
        'store/product_detail.html',
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

    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

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
        request, 'store/cart_detail.html', {'cart': cart})


def order_create(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        if form.is_valid():
            order = form.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity']
                )

            request.session['cart'] = {}

            return render(request, 'store/order_created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'store/order_create.html', {'cart': cart, 'form': form})
