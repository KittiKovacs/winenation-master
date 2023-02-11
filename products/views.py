from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product, Category
from .forms import ProductForm

from django.contrib.auth.decorators import login_required


def all_wines(request):
    """ A view to show all products, including sorting and search queries """

    wines = Product.objects.filter(is_a_subscription=False)
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                wines = wines.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            wines = wines.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            wines = wines.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('wines'))

            queries = Q(name__icontains=query) | Q(
                                                description__icontains=query)
            wines = wines.filter(queries)
    current_sorting = f'{sort}_{direction}'

    paginator = Paginator(wines, 16)
    page = request.GET.get('page')

    try:
        wines = paginator.page(page)
    except PageNotAnInteger:
        wines = paginator.page(1)
    except EmptyPage:
        wines = paginator.page(paginator.num_pages)

    context = {
        'wines': wines,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/wines.html', context)


def wine_details(request, product_id):

    wines = Product.objects.filter(is_a_subscription=False)
    wine = get_object_or_404(wines, pk=product_id)

    context = {
        'wine': wine,
    }

    return render(request, 'products/wine_details.html', context)


def all_subscriptions(request):
    """ A view to show all subscriptions """

    subscriptions = Product.objects.filter(is_a_subscription=True)

    context = {
        'subscriptions': subscriptions,
    }

    return render(request, 'products/subscriptions.html', context)


def about(request):

    return render(request, 'info/about.html')


@login_required
def add_product(request):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you dont have access to this feature.')
        return redirect(reverse('home'))
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')

            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. \
                           Please ensure the form is valid.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you dont have access to this feature.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            if 'wine' in request.POST:
                return redirect(reverse('wine_details', args=[product.id]))
            elif 'subscription' in request.POST:
                return redirect(reverse('subscriptions'))
        else:
            messages.error(request, 'Failed to update product.\
                 Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, you dont have access to this feature.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('wines'))
