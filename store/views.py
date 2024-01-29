from django.contrib.auth.models import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def login_page(request):
    title = 'Login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/home')
        else:
            messages.error(request, "alert-danger")
            return redirect('/')
    else:
        return render(request, 'login.html', {'title': title})

@login_required(login_url='/')
def logout_page(request):
    auth.logout(request)
    messages.info(request, "alert-success")
    return redirect('/')

@login_required(login_url='/')
def home_page(request):
    title = 'Home'
    return render(request, 'home.html', {'title': title})

@login_required(login_url='/')
def add_category(request):
    title = 'Add Category'
    categories = Category.objects.all()
    if request.method == 'POST':
        category = request.POST['c_name']
        if categories.filter(c_name=category).exists():
            messages.info(request, "Category already exists")
            return redirect('/add-category')
        else:
            new_category = Category(c_name=category)
            new_category.save()
            return redirect('/add-category')
    else:
        return render(request, 'add-category.html', {'title': title, 'categories': categories})

@login_required(login_url='/')
def delete_category(request, c_id):
    queryset = Category.objects.filter(id=c_id)
    queryset.delete()
    return redirect('/add-category')

@login_required(login_url='/')
def update_category(request, c_id):
    queryset = Category.objects.filter(id=c_id)
    queryset.update(c_name=request.POST['c_name'])
    return redirect('/add-category')


@login_required(login_url='/')
def add_product(request):
    title = 'Add Product'
    products = Product.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        product = request.POST['p_name']
        product_disc = request.POST['p_description']
        category_id = request.POST['c_name']
        if products.filter(p_name=product).exists():
            messages.info(request, "Product already exists")
            return redirect('/add-product')
        else:
            try:
                category = Category.objects.get(pk=category_id)
                new_product = Product(p_name=product, p_description=product_disc, c_name=category)
                new_product.save()
                return redirect('/add-product')
            except Category.DoesNotExist:
                messages.info(request, "Category does not exists")
    else:
        return render(request, 'add-product.html', {'title': title, 'products': products, 'categories': categories})


@login_required(login_url='')
def delete_product(request, p_id):
    queryset = Product.objects.filter(id=p_id)
    queryset.delete()
    return redirect('/add-product')

@login_required(login_url='')
def update_product(request, p_id):
    queryset = Product.objects.filter(id=p_id)
    product = request.POST['p_name']
    product_disc = request.POST['p_description']
    category_id = request.POST['c_name']
    category = Category.objects.get(pk=category_id)
    queryset.update(p_name=product, p_description=product_disc, c_name=category)
    return redirect('/add-product')


