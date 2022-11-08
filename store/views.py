
from urllib.parse import urlencode
from django.shortcuts import redirect, render, reverse
from numpy import squeeze
from store.models import SubCategory, Product, Contact
from django.core.paginator import Paginator
from cart.cart import Cart
from store.forms import *
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import viewsets, permissions
from store.serializers import ProductSerializer
import pandas as pd
import re, os
from django.conf import settings

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('-public_day')
    serializer_class = ProductSerializer
    # permission_classes = [permissions.IsAdminUser] # Đọc và ghi
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Chỉ đọc



def product_service(request):
    product = Product.objects.order_by('-public_day')
    result_list = list(product.values('name', 'price', 'content', 'image'))
    return JsonResponse(result_list, safe=False)

def product_service_number(request, pk):
    product = Product.objects.filter(pk=pk).order_by('-public_day')
    result_list = list(product.values('name', 'price'))[0]
    return JsonResponse(result_list, safe=False)




def index(request):
    cart = Cart(request)
    # Thiết bị gia đình
    tbgd_subcategory = SubCategory.objects.filter(category=1).values_list('id')
    tbgd_list_subcategory = []
    for subcategory in tbgd_subcategory:
        tbgd_list_subcategory.append(subcategory[0])
    tbgd_products = Product.objects.filter(subcategory__in=tbgd_list_subcategory).order_by('-public_day')

    # Đồ dùng nhà bếp
    ddnb_subcategory = SubCategory.objects.filter(category=2).values_list('id')
    ddnb_list_subcategory = []
    for subcategory in ddnb_subcategory:
        ddnb_list_subcategory.append(subcategory[0])
    ddnb_products = Product.objects.filter(subcategory__in=ddnb_list_subcategory).order_by('-public_day')

    return render(request, 'store/index.html', {
        'tbgd_products': tbgd_products[:21],
        'ddnb_products': ddnb_products[:21],
        'cart': cart,
    })


def subcategory(request, pk):
    cart = Cart(request)
    # Đọc danh sách danh mục sản phẩm (subcategory list)
    list_subcategory = SubCategory.objects.order_by('name')

    # Đọc danh sách sản phẩm theo danh mục
    if pk == 0:
        products = Product.objects.order_by('-public_day')
        subcategory_name = 'Tất cả sản phẩm (' + str(len(products)) + ')'
    else:
        products = Product.objects.filter(subcategory=pk).order_by('-public_day')
        selected_subcategory = SubCategory.objects.get(pk=pk)
        subcategory_name = selected_subcategory.name + ' (' + str(len(products)) + ')'

    # Lọc giá
    from_price = ''
    to_price = ''
    keyword = ''
    if request.GET.get('from_price'):
        from_price = int(request.GET.get('from_price'))
        to_price = int(request.GET.get('to_price'))
        keyword = request.GET.get('keyword')

        if keyword != '':
            products = Product.objects.filter(name__contains=keyword).order_by('price')

        products = [product for product in products if from_price <= product.price <= to_price]
        subcategory_name = '%i sản phẩm tìm thấy trong khoảng giá từ "%s" đến "%s"' % (len(products), "{:,}".format(from_price), "{:,}".format(to_price))

    # Phân trang
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 15)
    products_pager = paginator.page(page)

    # Sidebar slider
    # Tất cả sp
    if pk == 0:
        sub_product = Product.objects.order_by('-public_day')
    # Sp theo danh mục
    else:
        sub_product = Product.objects.filter(subcategory=pk).order_by('-public_day')


    return render(request, 'store/product-list.html', {
        'list_subcategory': list_subcategory,
        'products': products_pager,
        'subcategory_name': subcategory_name,
        'cart': cart,
        'from_price': from_price,
        'to_price': to_price,
        'keyword': keyword,
        'sub_product': sub_product[:21],
    })

def product(request, pk):
    cart = Cart(request)
    # Đọc danh sách danh mục sản phẩm (subcategory list)
    list_subcategory = SubCategory.objects.order_by('name')

    # Lấy thông tin sản phẩm
    product = Product.objects.get(pk=pk)

    # Tìm sản phẩm liên quan (cùng subcategory)
    subcategoryid = product.subcategory_id
    relate_products = Product.objects.filter(subcategory=subcategoryid).exclude(id=pk).order_by('-public_day')

    subcategory_name = SubCategory.objects.get(id=subcategoryid)

    # Rules
    rules = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'data_analysis/rules.csv'), squeeze=True, index_col=0)
    lst = rules.values.tolist()
    list_rules = []
    for item in lst:
        if str(pk) in re.findall('\d+[, \d+]*', item[0])[0].split(','):
            list_rules = re.findall('\d+[, \d+]*', item[1])[0].split(',')
    list_asc_products = []
    for i in list_rules:
        list_asc_products.append(Product.objects.get(pk=int(i)))


    return render(request, 'store/product-detail.html', {
        'list_subcategory': list_subcategory,
        'cart': cart,
        'product': product,
        'relate_products': relate_products,
        'subcategory_name': subcategory_name,
        'list_asc_products': list_asc_products,
    })


def search(request):
    cart = Cart(request)

    # Đọc danh sách danh mục sản phẩm (subcategory list)
    list_subcategory = SubCategory.objects.order_by('name')

    search_page = []
    result_search = ''
    if request.GET.get('keyword'):
        keyword = request.GET.get('keyword').strip()
        keyword_search = Product.objects.filter(name__contains=keyword).order_by('-public_day')
        result_search = '%i sản phẩm tìm thấy với từ khóa "%s"' % (len(keyword_search), keyword)

        page = request.GET.get('page', 1)
        paginator = Paginator(keyword_search, 15)
        search_page = paginator.page(page)
    
    # Lọc giá
    from_price = ''
    to_price = ''
    if request.GET.get('from_price'):
        from_price = int(request.GET.get('from_price'))
        to_price = int(request.GET.get('to_price'))

        base_url = reverse('store:subcategory', kwargs={'pk':0}) # <a href="{% url 'store:subcategory' 0%}"></a>
        query_string = urlencode({
            'from_price': from_price,
            'to_price': to_price,
            'keyword': keyword,
        })

        url = '%s?%s' % (base_url, query_string)
        return redirect(url)
        



    return render(request, 'store/product-list.html', {
        'products': search_page,
        'list_subcategory': list_subcategory,
        'cart': cart,
        'subcategory_name': result_search,
        'keyword': keyword,
    })

def contact(request):
    cart = Cart(request)

    result = ''
    form = FormContact()
    if request.POST.get('btnSendMessage'):
        form = FormContact(request.POST, Contact)
        if form.is_valid():
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.email = form.cleaned_data['email']
            post.phone_number = form.cleaned_data['phone_number']
            post.subject = form.cleaned_data['subject']
            post.message = form.cleaned_data['message']
            post.save()
            result = '''
            <div class="alert alert-success" role="alert">
                Gửi thành công! Chúng tôi sẽ liên hệ với bạn trong thời gian sớm nhất!
            </div>
            '''
            return redirect('store:contact')
    
    
    return render(request, 'store/contact.html', {
        'cart': cart,
        'result': result,
        'form': form,
    })


def demo_user(request):
    cart = Cart(request)
    frm_user = FormUser()
    frm_profile = FormUserProfileInfo()
    chuoi_kq_dang_ky = ''

    if request.POST.get('btnDangKy'):
        frm_user = FormUser(request.POST)
        frm_profile = FormUserProfileInfo(request.POST, request.FILES)
        if frm_user.is_valid() and frm_profile.is_valid():
            if frm_user.cleaned_data['password'] == frm_user.cleaned_data['confirm_password']:
                # Ghi vào CSDL
                user = frm_user.save()
                user.set_password(user.password)
                user.save()

                profile = frm_profile.save(commit=False)
                profile.user = user 
                profile.save()

                chuoi_kq_dang_ky = '''
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Đã đăng ký thông tin thành công.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store:user')

    return render(request, 'store/user.html', {
        'cart': cart,
        'frm_user': frm_user,
        'frm_profile': frm_profile,
        'chuoi_kq_dang_ky': chuoi_kq_dang_ky,
    })

def logout_user(request):
    logout(request)

    return redirect('store:user')
