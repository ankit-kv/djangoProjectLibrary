from multiprocessing import Value
from django.contrib.auth.models import auth
from django.db.models import ProtectedError, Sum, Count, Min, F, OuterRef, Case, When, Value, CharField
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta, datetime
import json

# Create your views here.
def is_admin(user):
    return user.is_authenticated and user.is_staff


def login_page(request):
    title = 'Login'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_staff:
                return redirect('/')
            else:
                return redirect('/request-items')
        else:
            messages.error(request, "alert-danger")
            return redirect('/login')
    else:
        return render(request, 'registration/login.html', {'title': title})

@login_required(login_url='/login')
def logout_page(request):
    auth.logout(request)
    messages.info(request, "alert-success")
    return redirect('/login')



@login_required(login_url='/login')
def home_page(request):
    if request.user.is_authenticated and request.user.is_staff:
        stored_messages = request.session.pop('stored_messages', [])
        title = 'Dashboard'
        transaction = Transaction.objects.order_by('-t_date_time')[:10]
        products = Product.objects.all()
        issued = Transaction.objects.filter(issued_quantity__gt=0).values('product').annotate(total=Sum('issued_quantity')).order_by('-total')[:10]
        received = Transaction.objects.filter(received_quantity__gt=0).values('product').annotate(
            total=Sum('received_quantity')).order_by('-total')[:10]
        class_name = 'fa-solid fa-gauge-high'
        return render(request, 'home.html', {'title': title, 'class_name': class_name, 'messages_for_admin': stored_messages,
                                             'transactions': transaction, 'issued': issued, 'received': received, 'products': products})
    else:
        return redirect('/request-items')


@user_passes_test(is_admin)
@login_required(login_url='/login')
def add_category(request):
    title = 'Add Category'
    class_name = 'fa-solid fa-layer-group'
    search = request.GET.get('search')
    if search is not None:
        categories = Category.objects.filter(c_name__icontains=search)
    else:
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
        return render(request, 'category/add-category.html', {'title': title, 'categories': categories, 'class_name': class_name})


@user_passes_test(is_admin)
@login_required(login_url='/login')
def delete_category(request, c_id):
    queryset = Category.objects.filter(id=c_id)
    try:
        queryset.delete()
        return redirect('/add-category')
    except ProtectedError:
        messages.info(request, "Category cannot be deleted because it has some product associated with it")
        return redirect('/add-category')


@user_passes_test(is_admin)
@login_required(login_url='/login')
def update_category(request, c_id):
    queryset = Category.objects.filter(id=c_id)
    queryset.update(c_name=request.POST['c_name'])
    return redirect('/add-category')


@user_passes_test(is_admin)
@login_required(login_url='/login')
def add_product(request):
    title = 'Add Product'
    class_name = 'fa-solid fa-plus'
    search = request.GET.get('search')
    if search is not None:
        products = Product.objects.filter(p_name__icontains=search)
    else:
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
        return render(request, 'product/add-product.html', {'title': title, 'products': products, 'categories': categories, 'class_name': class_name})


@user_passes_test(is_admin)
@login_required(login_url='/login')
def delete_product(request, p_id):
    queryset = Product.objects.get(id=p_id)
    if queryset.quantity == 0:
        queryset.delete()
        return redirect('/add-product')
    else:
        messages.info(request, "Product can not be deleted because it has some balance quantity")
        return redirect('/add-product')


@user_passes_test(is_admin)
@login_required(login_url='/login')
def update_product(request, p_id):
    queryset = Product.objects.filter(id=p_id)
    product = request.POST['p_name']
    product_disc = request.POST['p_description']
    category_id = request.POST['c_name']
    category = Category.objects.get(pk=category_id)
    queryset.update(p_name=product, p_description=product_disc, c_name=category)
    return redirect('/add-product')


@user_passes_test(is_admin)
@login_required(login_url='/login')
def add_section(request):
    title = 'Add Section'
    class_name = 'fa-solid fa-folder-plus'
    sections = Section.objects.all()
    if request.method == 'POST':
        section_name = request.POST['section_name']
        if sections.filter(section_name=section_name).exists():
            messages.info(request, "Section already exists")
            return redirect('/add-section')
        else:
            section = Section(section_name=section_name)
            section.save()
            return redirect('/add-section')
    else:
        return render(request, 'section/add-section.html', {'title': title, 'sections': sections, 'class_name': class_name})


@user_passes_test(is_admin)
@login_required(login_url='/login')
def delete_section(request, sec_id):
    queryset = Section.objects.filter(id=sec_id)
    queryset.delete()
    return redirect('/add-section')


@user_passes_test(is_admin)
@login_required(login_url='/login')
def update_section(request, sec_id):
    queryset = Section.objects.filter(id=sec_id)
    queryset.update(section_name=request.POST['section_name'])
    return redirect('/add-section')


@user_passes_test(is_admin)
@login_required(login_url='/login')
def add_staff(request):
    title = 'Add Staff'
    class_name = 'fa-solid fa-user-plus'
    search = request.GET.get('search')
    if search is not None:
        staff = Staff.objects.filter(staff_name__icontains=search)
    else:
        staff = Staff.objects.all()
    sections = Section.objects.all()
    if request.method == 'POST':
        staff_name = request.POST['staff_name']
        email = request.POST['staff_email']
        phone = request.POST['staff_phone']
        section = request.POST['staff_section']
        if staff.filter(staff_email=email).exists():
            messages.info(request,"Staff already Exists")
            return redirect('/add-staff')
        else:
            staff = Staff(staff_name=staff_name, staff_email=email, staff_phone=phone, staff_section=section)
            staff.save()
            return redirect('/add-staff')
    else:
        return render(request, 'staff/add-staff.html', {'title': title, 'staffs': staff, 'class_name': class_name, 'sections': sections})


@user_passes_test(is_admin)
@login_required(login_url='/login')
def delete_staff(request, s_id):
    queryset = Staff.objects.filter(id=s_id)
    queryset.delete()
    return redirect('/add-staff')


@user_passes_test(is_admin)
@login_required(login_url='/login')
def update_staff(request, s_id):
    queryset = Staff.objects.filter(id=s_id)
    staff_name = request.POST['staff_name']
    staff_email = request.POST['staff_email']
    staff_phone = request.POST['staff_phone']
    staff_section = request.POST['staff_section']
    queryset.update(staff_name=staff_name, staff_email=staff_email, staff_phone=staff_phone, staff_section=staff_section)
    return redirect('/add-staff')


@user_passes_test(is_admin)
@login_required(login_url='/login')
def receive_items(request):
    products = Product.objects.all()
    transactions = Transaction.objects.filter(received_quantity__gt=0).order_by('-t_date_time')[:10]
    staffs = Staff.objects.all()
    sections = Section.objects.all()
    title = 'Receive Items'
    class_name = 'fa-regular fa-circle-down'
    context = {'title': title, 'products': products, 'transactions': transactions, 'class_name': class_name,'staffs': staffs, 'sections': sections}
    if request.method == 'POST':
        staff = request.POST['received_from_staff']
        section = request.POST['received_from_section']
        vendor = request.POST['received_from_vendor']
        if staff == "staff":
            if section == "section":
                receiver = vendor
            else:
                receiver = Section.objects.get(id=section)
                receiver = receiver.section_name
        else:
            receiver = Staff.objects.get(id=staff)
            receiver = receiver.staff_name

        product_id = request.POST['product']
        received_quantity = request.POST['received_quantity']
        date_time = timezone.now()
        user = request.user
        product = Product.objects.get(id=product_id)
        transaction = Transaction(t_date_time=date_time, user=user.first_name, product=product.p_name,
                                  category=product.c_name.c_name, received_quantity=received_quantity, received_from=receiver)
        product.quantity = product.quantity + int(received_quantity)
        transaction.save()
        product.save()
        if not receiver == vendor:
            try:
                recipient = Recipient.objects.get(rec_name=receiver, product=product)
                if int(received_quantity) <= recipient.rec_quantity:
                    recipient.rec_quantity = recipient.rec_quantity - int(received_quantity)
                    recipient.save()
                else:
                    messages.info(request, "Received quantity is more than issued")
            except Recipient.DoesNotExist:
                messages.info(request, 'Recipient does not exist')
            return redirect('/receive-item')
        else:
            return redirect('/receive-item')
    else:
        return render(request, 'items/received-items.html', context=context)



@user_passes_test(is_admin)
@login_required(login_url='/login')
def issue_items(request):
    products = Product.objects.all()
    transactions = Transaction.objects.filter(issued_quantity__gt=0).order_by('-t_date_time')[:10]
    staff = Staff.objects.all()
    sections = Section.objects.all()
    title = 'Issue Items'
    class_name = 'fa-regular fa-circle-up'
    context = {'title': title, 'products': products, 'transactions': transactions, 'staffs': staff, 'class_name': class_name, 'sections': sections}
    if request.method == 'POST':
        product_id = request.POST['product']
        issued_quantity = request.POST['issued_quantity']
        date_time = timezone.now()
        user = request.user
        staff = request.POST['issued_to_staff']
        section = request.POST['issued_to_section']
        if staff == "staff":
            issued_to = Section.objects.get(id=section)
            issued_to = issued_to.section_name
        else:
            issued_to = Staff.objects.get(id=staff)
            issued_to = issued_to.staff_name
        product = Product.objects.get(id=product_id)
        transaction = Transaction(t_date_time=date_time, user=user.first_name, product=product.p_name, category=product.c_name.c_name, issued_quantity=issued_quantity, issued_to=issued_to)
        if int(issued_quantity) > product.quantity:
            messages.info(request, 'You do not have enough items to issue')
            return redirect('/issue-item')
        else:
            product.quantity = product.quantity - int(issued_quantity)
            transaction.save()
            product.save()
            try:
                recipient = Recipient.objects.get(rec_name=issued_to, product=product)
                recipient.rec_quantity = recipient.rec_quantity + int(issued_quantity)
                recipient.save()
            except Recipient.DoesNotExist:
                recipient = Recipient(rec_name=issued_to, product=product, rec_quantity=issued_quantity)
                recipient.save()
            return redirect('/issue-item')
    else:
        return render(request, 'items/issued-items.html', context)



@user_passes_test(is_admin)
@login_required(login_url='/login')
def list_all_items(request):
    title = 'All Items'
    class_name = 'fa-regular fa-newspaper'
    search = request.GET.get('search')
    if search is not None:
        products = Product.objects.filter(p_name__icontains=search)
    else:
        products = Product.objects.all()
    return render(request, 'items/list_all_items.html', {'title': title, 'products': products, 'class_name': class_name})


@user_passes_test(is_admin)
@login_required(login_url='/login')
def all_transaction(request):
    title = 'All Transactions'
    category = Category.objects.all()
    class_name = 'fa-solid fa-arrow-right-arrow-left'
    transactions = Transaction.objects.all().order_by('-t_date_time')
    if request.method == 'POST':
        filter_box = request.POST.get('filter')
        category_name = request.POST.get('c_name')
        value = request.POST.get('value')
        if filter_box == "1":
            transactions = Transaction.objects.filter(product__contains=value)
        elif filter_box == "2":
            transactions = Transaction.objects.filter(category=category_name)
        elif filter_box == "3":
            transactions = Transaction.objects.filter(received_quantity__gte=value)
        elif filter_box == "4":
            transactions = Transaction.objects.filter(issued_quantity__gte=value)
        elif filter_box == "5":
            from_date = request.POST.get('from_date')
            to_date = datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d') + timedelta(days=1)
            transactions = Transaction.objects.filter(t_date_time__gte=from_date, t_date_time__lte=to_date)
        else:
            transactions = Transaction.objects.all()
        context = {'title': title, 'categories': category, 'transactions': transactions, 'class_name': class_name}
        return render(request,'items/all-transactions.html', context)
    else:
        context = {'title': title, 'categories': category, 'transactions': transactions, 'class_name': class_name}
        return render(request, 'items/all-transactions.html', context)


@user_passes_test(is_admin)
@login_required(login_url='/login')
def list_issued_transaction(request):
    title = 'Issued Transactions'
    category = Category.objects.all()
    class_name = 'fa-regular fa-newspaper'
    transactions = Transaction.objects.filter(issued_quantity__gt=0).order_by('-t_date_time')
    total = transactions.aggregate(Sum('issued_quantity'))['issued_quantity__sum']
    if request.method == 'POST':
        filter_box = request.POST.get('filter')
        category_name = request.POST.get('c_name')
        value = request.POST.get('value')
        if filter_box == "1":
            transactions = Transaction.objects.filter(product__contains=value, issued_quantity__gt=0)
            total = transactions.aggregate(Sum('issued_quantity'))['issued_quantity__sum']
        elif filter_box == "2":
            transactions = Transaction.objects.filter(category=category_name, issued_quantity__gt=0)
            total = transactions.aggregate(Sum('issued_quantity'))['issued_quantity__sum']
        elif filter_box == "3":
            transactions = Transaction.objects.filter(issued_quantity__gte=value)
            total = transactions.aggregate(Sum('issued_quantity'))['issued_quantity__sum']
        elif filter_box == "4":
            from_date = request.POST.get('from_date')
            to_date = datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d') + timedelta(days=1)
            transactions = Transaction.objects.filter(t_date_time__gte=from_date, t_date_time__lte=to_date, issued_quantity__gt=0)
            total = transactions.aggregate(Sum('issued_quantity'))['issued_quantity__sum']
        else:
            transactions = Transaction.objects.filter(issued_quantity__gt=0).order_by('-t_date_time')
            total = transactions.aggregate(Sum('issued_quantity'))['issued_quantity__sum']
        context = {'title': title, 'categories': category, 'transactions': transactions, 'class_name': class_name, 'total': total}
        return render(request,'items/list_issued_items.html', context)
    else:
        context = {'title': title, 'categories': category, 'transactions': transactions, 'class_name': class_name, 'total': total}
        return render(request, 'items/list_issued_items.html', context)


@user_passes_test(is_admin)
@login_required(login_url='/login')
def list_received_transaction(request):
    title = 'Received Transactions'
    category = Category.objects.all()
    class_name = 'fa-solid fa-rectangle-list'
    transactions = Transaction.objects.filter(received_quantity__gt=0).order_by('-t_date_time')
    total = transactions.aggregate(Sum('received_quantity'))['received_quantity__sum']
    if request.method == 'POST':
        filter_box = request.POST.get('filter')
        category_name = request.POST.get('c_name')
        value = request.POST.get('value')
        if filter_box == "1":
            transactions = Transaction.objects.filter(product__contains=value,received_quantity__gt=0)
            total = transactions.aggregate(Sum('received_quantity'))['received_quantity__sum']
        elif filter_box == "2":
            transactions = Transaction.objects.filter(category=category_name,received_quantity__gt=0)
            total = transactions.aggregate(Sum('received_quantity'))['received_quantity__sum']
        elif filter_box == "3":
            transactions = Transaction.objects.filter(received_quantity__gte=value)
            total = transactions.aggregate(Sum('received_quantity'))['received_quantity__sum']
        elif filter_box == "4":
            from_date = request.POST.get('from_date')
            to_date = datetime.strptime(request.POST.get('to_date'), '%Y-%m-%d') + timedelta(days=1)
            transactions = Transaction.objects.filter(t_date_time__gte=from_date, t_date_time__lte=to_date, received_quantity__gt=0)
            total = transactions.aggregate(Sum('received_quantity'))['received_quantity__sum']
        else:
            transactions = Transaction.objects.all()
        context = {'title': title, 'categories': category, 'transactions': transactions, 'class_name': class_name, 'total': total}
        return render(request,'items/list_received_items.html', context)
    else:
        context = {'title': title, 'categories': category, 'transactions': transactions, 'class_name': class_name, 'total': total}
        return render(request, 'items/list_received_items.html', context)



@user_passes_test(is_admin)
@login_required(login_url='/login')
def staff_details(request, s_id):
    title = 'Staff Details'
    staff = Staff.objects.get(id=s_id)
    recipients = Recipient.objects.filter(rec_name=staff.staff_name)
    return render(request, 'staff/staff-details.html', {'title': title, 'staff': staff, 'recipients':recipients})


@user_passes_test(is_admin)
@login_required(login_url='/login')
def section_details(request, sec_id):
    title = 'Section Details'
    section = Section.objects.get(id=sec_id)
    recipients = Recipient.objects.filter(rec_name=section.section_name)
    return render(request, 'section/section-details.html', {'title': title, 'section': section, 'recipients':recipients})


@login_required(login_url='/login')
def request_items(request):
    title = 'Request Items'
    class_name = 'fa-regular fa-hand'
    products = Product.objects.all()
    if request.method == 'POST':
        product_table_data = request.POST.get('product_table_data', '[]')
        if len(product_table_data) != 0:
            tracking_id = str(uuid.uuid4())
            user = request.user
            date_time = datetime.now()
            product_table_data = json.loads(product_table_data)
            for item in product_table_data:
                product_name = item['productName']
                quantity = item['productQuantity']
                request_item = Request_Items.objects.create(tracking_id=tracking_id, product_name=product_name, quantity=quantity, date_time=date_time, user=user)
                request_item.save()
            messages.success(request, 'Your request has been submitted')
            return redirect('/request-items')
        else:
            messages.info(request, 'Please add some products')
        return redirect('request_items')
    else:
        return render(request, 'request-form/request-form.html', {'title': title, 'class_name': class_name,'products': products})


@login_required(login_url='/login')
def items_in_store(request):
    title = 'All Items in Store'
    class_name = 'fa-solid fa-table-cells'
    search = request.GET.get('search')
    if search is not None:
        products = Product.objects.filter(p_name__icontains=search)
    else:
        products = Product.objects.all()
    return render(request, 'request-form/all-items.html',
                  {'title': title, 'products': products, 'class_name': class_name})


@login_required(login_url='/login')
def request_history(request):
    title = 'Request History'
    class_name = 'fa-solid fa-clock-rotate-left'
    request_items = Request_Items.objects.filter(user=request.user).values('tracking_id').annotate(count=Count('id'), date=Min('date_time')).order_by('-date')

    return render(request, 'request-form/request-history.html', {'title': title, 'request_items': request_items, 'class_name': class_name})


@login_required(login_url='/login')
def request_detail(request, t_id):
    title = 'Request History Detail'
    class_name = 'fa-solid fa-circle-info'
    request_items = Request_Items.objects.filter(tracking_id=t_id)
    return render(request, 'request-form/request-detail.html', {'title': title, 'request_items': request_items, 'class_name': class_name})


@user_passes_test(is_admin)
@login_required(login_url='/login')
def all_requests(request):
    title = 'All Requests'
    class_name = 'fa-regular fa-hand'
    users = User.objects.all()
    tracking_ids = Request_Items.objects.values('tracking_id').order_by('-id')
    unique_tracking_ids = []
    for tracking_id in tracking_ids:
        if tracking_id.get('tracking_id') not in unique_tracking_ids:
            unique_tracking_ids.append(tracking_id.get('tracking_id'))
    tracking_info_list = []
    for tracking_id in unique_tracking_ids:
        tracking_data = Request_Items.objects.filter(tracking_id=tracking_id)

        total_count = tracking_data.count()
        first_row_datetime = tracking_data.aggregate(Min('date_time'))['date_time__min']
        first_row_user = tracking_data.first().user if total_count > 0 else None

        tracking_info_list.append({
            'tracking_id': tracking_id,
            'total_count': total_count,
            'first_row_datetime': first_row_datetime,
            'first_row_user': first_row_user,
        })
    return render(request, 'request-to/all-requests.html', {'title': title, 'tracking_info_list': tracking_info_list, 'class_name': class_name})


@user_passes_test(is_admin)
@login_required(login_url='/login')
def show_request_detail(request, t_id):
    title = 'Request Detail'
    class_name = 'fa-solid fa-circle-info'
    products = Product.objects.all()
    request_items = Request_Items.objects.filter(tracking_id=t_id).annotate(
        balance=Product.objects.filter(p_name=OuterRef('product_name')).values('quantity')[:1],
        available=Case(
            When(
                quantity__lte=F('balance'),
                then=Value('Available', output_field=CharField())
            ),
            When(
                quantity__gt=F('balance'),
                then=Value('Out of Stock', output_field=CharField())
            ),
            default=Value('No', output_field=CharField())
        )
    )

    first = Request_Items.objects.filter(tracking_id=t_id).first()
    return render(request, 'request-to/detail.html', {'title': title, 'request_items': request_items, 'class_name': class_name, 'first': first})
