from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import MyUser, Book, Img, Item, Order, OrderItem
from django.core.urlresolvers import reverse
from management.utils import permission_check
import datetime
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'management/index.html', content)


def signup(request):
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/signup.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'management/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'management/set_password.html', content)


@user_passes_test(permission_check)
def add_book(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_book = Book(
            name=request.POST.get('name', ''),
            author=request.POST.get('author', ''),
            category=request.POST.get('category', ''),
            price=request.POST.get('price', 0),
            publish_date=request.POST.get('publish_date', '')
        )
        new_book.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_book',
        'state': state,
    }
    return render(request, 'management/add_book.html', content)


def view_book_list(request):
    user = request.user if request.user.is_authenticated() else None
    category_list = Book.objects.values_list('category', flat=True).distinct()
    query_category = request.GET.get('category', 'all')
    if (not query_category) or Book.objects.filter(category=query_category).count() is 0:
        query_category = 'all'
        book_list = Book.objects.all()
    else:
        book_list = Book.objects.filter(category=query_category)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        book_list = Book.objects.filter(name__contains=keyword)
        query_category = 'all'

    paginator = Paginator(book_list, 5)
    page = request.GET.get('page')
    try:
        book_list = paginator.page(page)
    except PageNotAnInteger:
        book_list = paginator.page(1)
    except EmptyPage:
        book_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_book',
        'category_list': category_list,
        'query_category': query_category,
        'book_list': book_list,
    }
    return render(request, 'management/view_book_list.html', content)


def detail(request):
    user = request.user if request.user.is_authenticated() else None
    book_id = request.GET.get('id', '')
    if book_id == '':
        return HttpResponseRedirect(reverse('view_book_list'))
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return HttpResponseRedirect(reverse('view_book_list'))
    content = {
        'user': user,
        'active_menu': 'view_book',
        'book': book,
    }
    return render(request, 'management/detail.html', content)


@user_passes_test(permission_check)
def add_img(request):
    user = request.user
    state = None
    if request.method == 'POST':
        try:
            new_img = Img(
                name=request.POST.get('name', ''),
                description=request.POST.get('description', ''),
                img=request.FILES.get('img', ''),
                book=Book.objects.get(pk=request.POST.get('book', ''))
            )
            new_img.save()
        except Book.DoesNotExist as e:
            state = 'error'
            print(e)
        else:
            state = 'success'
    content = {
        'user': user,
        'state': state,
        'book_list': Book.objects.all(),
        'active_menu': 'add_img',
    }
    return render(request, 'management/add_img.html', content)


# item

@user_passes_test(permission_check)
def add_item(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_item = Item(
            id_item=request.POST.get('id_item', ''),
            name_dish=request.POST.get('name_dish', ''),
            price=request.POST.get('price', 0),
            start_date=request.POST.get('start_date', ''),
            photo_item=request.FILES.get('start'),
        )
        new_item.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_item',
        'state': state,
    }
    return render(request, 'management/add_item.html', content)


def view_item_list(request):
    user = request.user if request.user.is_authenticated() else None
    items = Item.objects.all()
    query_category = 'all'
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        items = Item.objects.filter(id_item__contains=keyword)

    paginator = Paginator(items, 5)
    page = request.GET.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    content = {
        'user': user,
        'active_menu': 'view_item',
        'items': items,
        'query_category': query_category,
    }
    return render(request, 'management/view_item_list.html', content)


def item_detail(request):
    user = request.user if request.user.is_authenticated() else None
    item_id = request.GET.get('id', '')
    if item_id == '':
        return HttpResponseRedirect(reverse('view_item_list'))
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        return HttpResponseRedirect(reverse('view_item_list'))
    content = {
        'user': user,
        'active_menu': 'view_item',
        'item': item,
    }
    return render(request, 'management/item_detail.html', content)


def delItem(request):
    user = request.user if request.user.is_authenticated() else None
    item_id = request.GET.get('id', '')
    Item.objects.filter(id=item_id).delete()
    content = {
        'user': user,
        'active_menu': 'delItem',

    }

    return render(request, 'management/delItem.html', content)


def editItem(request):
    user = request.user
    state = None
    item_id = request.GET.get('id', '')
    if item_id == '':
        return HttpResponseRedirect(reverse('view_item_list'))
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        return HttpResponseRedirect(reverse('view_item_list'))
    if request.method == 'POST':
        item.price = request.POST.get('price', 0)
        item.save()

        state = 'success'
    content = {
        'user': user,
        'active_menu': 'eddItem',
        'state': state,
    }
    return render(request, 'management/editItem.html', content)


# user
def view_user_list(request):
    user = request.user if request.user.is_authenticated() else None
    users = MyUser.objects.all()
    query_category = 'all'
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        users = MyUser.objects.filter(nickname__contains=keyword)

    paginator = Paginator(users, 5)
    page = request.GET.get('page')

    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    content = {
        'user': user,
        'active_menu': 'view_user',
        'users': users,
        'query_category': query_category,
    }
    return render(request, 'management/view_user_list.html', content)


def delUser(request):
    user = request.user if request.user.is_authenticated() else None
    user_id = request.GET.get('id', '')
    MyUser.objects.filter(id=user_id).delete()
    content = {
        'user': user,
        'active_menu': 'delUser',

    }

    return render(request, 'management/delUser.html', content)


# order

def add_order(request):
    user = request.user
    state = None
    now = datetime.datetime.now()
    time = now
    data = now.strftime('%Y%m%d%H%M%S') + '00' + str(random.randint(10, 20))
    new_order = Order(
        id_order=data,
        time_order=time,
        total=0,

    )
    new_order.save()
    state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_order',
        'state': state,
        'order': new_order

    }
    return render(request, 'management/add_order.html', content)


def view_order_list(request):
    user = request.user if request.user.is_authenticated() else None
    time_list = Order.objects.values_list('id_order', flat=True).distinct()
    arr = []
    for time in time_list:
        if time[0:8] not in arr:
            arr.append(time[0:8])
    query_time = request.GET.get('time', 'all')
    qt = str(query_time)
    if (not query_time):
        query_time = 'all'
        orders = Order.objects.all()
    else:
        format = '0123456789'
        for c in query_time:
            if c not in format:
                qt = qt.replace(c, '')
        orders = Order.objects.filter(id_order__contains=qt)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        orders = Order.objects.filter(id_order__contains=keyword)
        query_time = 'all'

    r_total = 0
    for ord in orders:
        r_total += ord.total
    paginator = Paginator(orders, 5)
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    content = {
        'user': user,
        'active_menu': 'view_order',
        'orders': orders,
        'time_list': arr,
        'query_time': query_time,
        'r_total': r_total,
    }
    return render(request, 'management/view_order_list.html', content)


def order_detail(request):
    user = request.user if request.user.is_authenticated() else None
    order_id = request.GET.get('id', '')
    if order_id == '':
        return HttpResponseRedirect(reverse('view_order_list'))
    try:
        od = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return HttpResponseRedirect(reverse('view_order_list'))

    orderIt = od.orderitem_set.all()
    total = 0
    for oI in orderIt:
        total += oI.total()
    od.total = total
    od.save()

    paginator = Paginator(orderIt, 5)
    page = request.GET.get('page')
    try:
        orderIt = paginator.page(page)
    except PageNotAnInteger:
        orderIt = paginator.page(1)
    except EmptyPage:
        orderIt = paginator.page(paginator.num_pages)

    content = {
        'user': user,
        'active_menu': 'view_order',
        'order': od,
        'orderItem': orderIt,
    }
    return render(request, 'management/order_detail.html', content)


def delOrder(request):
    user = request.user if request.user.is_authenticated() else None
    user_id = request.GET.get('id', '')
    Order.objects.filter(id=user_id).delete()
    content = {
        'user': user,
        'active_menu': 'delOrder',

    }

    return render(request, 'management/delOrder.html', content)


# order_item

def add_orderItem(request):
    user = request.user
    state = None
    order_id = request.GET.get('id', '')
    od = Order.objects.get(pk=order_id)
    now = datetime.datetime.now()
    data = now.strftime('%Y%m%d%H%M%S')
    if request.method == 'POST':
        try:
            new_orderItem = OrderItem(
                id_OI=data,
                id_item=Item.objects.get(pk=request.POST.get('item', ())),
                id_order=od,
                item_total=request.POST.get('item_total', ''),
            )
            new_orderItem.save()
        except Item.DoesNotExist as e:
            state = 'error'
            print(e)
        else:
            state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_orderItem',
        'state': state,
        'item_list': Item.objects.all(),
        'od': od,
    }
    return render(request, 'management/add_orderItem.html', content)


def editOrderItem(request):
    user = request.user
    state = None
    od_id=request.GET.get('od', '')
    order_i=Order.objects.get(pk=od_id)
    order_id = request.GET.get('id', '')
    if order_id == '':
        return HttpResponseRedirect(reverse('view_order_list'))
    try:
        od = OrderItem.objects.get(pk=order_id)
    except OrderItem.DoesNotExist:
        return HttpResponseRedirect(reverse('view_order_list'))
    if request.method == 'POST':
        od.item_total = request.POST.get('item', 0)
        od.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'eddOrderItem',
        'state': state,
        'od': od,
        'order':order_i,
    }
    return render(request, 'management/editOrderItem.html', content)


def delOrderItem(request):
    user = request.user if request.user.is_authenticated() else None
    user_id = request.GET.get('id', '')
    od_id=request.GET.get('od', '')
    order_i=Order.objects.get(pk=od_id)
    OrderItem.objects.filter(id=user_id).delete()
    content = {
        'user': user,
        'active_menu': 'delUser',
        'order':order_i,

    }
    return render(request, 'management/delOrderItem.html', content)
