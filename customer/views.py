
from django.shortcuts import render, redirect
from customer.forms import FormDangKy, FormDangKy2
from customer.models import KhachHang
from cart.cart import Cart
from django.contrib.auth.hashers import Argon2PasswordHasher
from customer.my_module import read_json_internet

def customer_login_signup_2(request):
    cart = Cart(request)
    # Kiểm tra session của tài khoản đã đăng nhập chưa?
    if 's_khach_hang' in request.session:
        return redirect('store:index')

    # Load thông tin selection địa chỉ
    info = read_json_internet('http://api.laptrinhpython.net/vietnam') # Trả ra list
    lst_province = []
    lst_district = []
    lst_ward = []
    data_district = []

    for province in info:
        lst_province.append(province['name'])

        districts = []
        for district in province['districts']:
            d = district['prefix'] + ' ' + district['name']
            districts.append(d)
            data_district.append(d)


            wards = []
            for ward in district['wards']:
                w = ward['prefix'] + ' ' + ward['name']
                wards.append(w)
            else:
                str_wards = '|'.join(wards)
                lst_ward.append(str_wards)
        else:
            str_district='|'.join(districts)
            lst_district.append(str_district)


    # ĐĂNG KÝ
    frm_dang_ky = FormDangKy2()
    chuoi_kq_dang_ky = ''
    if request.POST.get('btnDangKy'):
        frm_dang_ky = FormDangKy2(request.POST, KhachHang)
        if frm_dang_ky.is_valid() and frm_dang_ky.cleaned_data['mat_khau'] == frm_dang_ky.cleaned_data['xac_nhan_mat_khau']:
            # hasher = PBKDF2PasswordHasher() #salt tối thiếu 1 byte(1 ký tự)
            hasher = Argon2PasswordHasher() #salt tối thiểu 8 bytes
            request.POST.__mutable = True
            post = frm_dang_ky.save(commit=False)
            post.ho = frm_dang_ky.cleaned_data['ho']
            post.ten = frm_dang_ky.cleaned_data['ten']
            post.email = frm_dang_ky.cleaned_data['email']
            post.mat_khau = hasher.encode(frm_dang_ky.cleaned_data['mat_khau'], '12345678')
            post.dien_thoai = frm_dang_ky.cleaned_data['dien_thoai']
            post.dia_chi = frm_dang_ky.cleaned_data['dia_chi'] + ', ' + frm_dang_ky.cleaned_data['phuong_xa'] \
                                                               + ', ' + frm_dang_ky.cleaned_data['quan_huyen'] \
                                                               + ', ' + frm_dang_ky.cleaned_data['tinh_tp']
            post.save()
            chuoi_kq_dang_ky = '''
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Đã đăng ký thông tin thành công.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''

    # ĐĂNG NHẬP
    chuoi_kq_dang_nhap = ''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = Argon2PasswordHasher()
        encoded = hasher.encode(mat_khau, '12345678')

        # Đọc dữ liệu từ CSDL
        khach_hang = KhachHang.objects.filter(email=email, mat_khau=encoded)
        if khach_hang.count() > 0:
            # Tạo session
            request.session['s_khach_hang'] = khach_hang.values()[0]  # [{'id': 1, 'ho': 'Lê Ngọc', 'ten': 'Trí', 'email': 'lengoctri.it.92@gmail.com', 'mat_khau': '123', 'dien_thoai': '0902377795', 'dia_chi': 'TPHCM'}]
            # print(request.session['s_khach_hang'])
            return redirect('store:index')
        else:
            chuoi_kq_dang_nhap = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Đăng nhập không thành công. Vui lòng kiểm tra lại.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''

    return render(request, 'store/login_2.html', {
        'frm_dang_ky': frm_dang_ky,
        'chuoi_kq_dang_ky': chuoi_kq_dang_ky,
        'chuoi_kq_dang_nhap': chuoi_kq_dang_nhap,
        'cart': cart,
        'lst_province': tuple(lst_province),
        'lst_district': tuple(lst_district),
        'lst_ward': tuple(lst_ward),
        'data_district': data_district,
    })

# Create your views here.
def customer_login_signup(request):
    cart = Cart(request)
    # Kiểm tra session của tài khoản đã đăng nhập chưa?
    if 's_khach_hang' in request.session:
        return redirect('store:index')

    # ĐĂNG KÝ
    frm_dang_ky = FormDangKy()
    chuoi_kq_dang_ky = ''
    if request.POST.get('btnDangKy'):
        frm_dang_ky = FormDangKy(request.POST, KhachHang)
        if frm_dang_ky.is_valid() and frm_dang_ky.cleaned_data['mat_khau'] == frm_dang_ky.cleaned_data['xac_nhan_mat_khau']:
            # hasher = PBKDF2PasswordHasher() #salt tối thiếu 1 byte(1 ký tự)
            hasher = Argon2PasswordHasher() #salt tối thiểu 8 bytes
            request.POST.__mutable = True
            post = frm_dang_ky.save(commit=False)
            post.ho = frm_dang_ky.cleaned_data['ho']
            post.ten = frm_dang_ky.cleaned_data['ten']
            post.email = frm_dang_ky.cleaned_data['email']
            post.mat_khau = hasher.encode(frm_dang_ky.cleaned_data['mat_khau'], '12345678')
            post.dien_thoai = frm_dang_ky.cleaned_data['dien_thoai']
            post.dia_chi = frm_dang_ky.cleaned_data['dia_chi']
            post.save()
            chuoi_kq_dang_ky = '''
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Đã đăng ký thông tin thành công.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''

    # ĐĂNG NHẬP
    chuoi_kq_dang_nhap = ''
    if request.POST.get('btnDangNhap'):
        # Gán biến
        email = request.POST.get('email')
        mat_khau = request.POST.get('mat_khau')
        hasher = Argon2PasswordHasher()
        encoded = hasher.encode(mat_khau, '12345678')

        # Đọc dữ liệu từ CSDL
        khach_hang = KhachHang.objects.filter(email=email, mat_khau=encoded)
        if khach_hang.count() > 0:
            # Tạo session
            request.session['s_khach_hang'] = khach_hang.values()[0]  # [{'id': 1, 'ho': 'Lê Ngọc', 'ten': 'Trí', 'email': 'lengoctri.it.92@gmail.com', 'mat_khau': '123', 'dien_thoai': '0902377795', 'dia_chi': 'TPHCM'}]
            # print(request.session['s_khach_hang'])
            return redirect('store:index')
        else:
            chuoi_kq_dang_nhap = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Đăng nhập không thành công. Vui lòng kiểm tra lại.
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''

    return render(request, 'store/login.html', {
        'frm_dang_ky': frm_dang_ky,
        'chuoi_kq_dang_ky': chuoi_kq_dang_ky,
        'chuoi_kq_dang_nhap': chuoi_kq_dang_nhap,
        'cart': cart,
    })


def customer_logout(request):
    if 's_khach_hang' in request.session:
        del request.session['s_khach_hang']
    return redirect('customer:login')

def my_account(request):
    cart = Cart(request)
    # Kiểm tra session của tài khoản đã đăng nhập chưa?
    if 's_khach_hang' not in request.session:
        return redirect('customer:login')
    
    # Cập nhật thông tin
    if request.POST.get('btnCapNhat'):
        # Gán biến
        ho = request.POST.get('ho')
        ten = request.POST.get('ten')
        dien_thoai = request.POST.get('dien_thoai')
        dia_chi = request.POST.get('dia_chi')

        # Cập nhật
        s_khach_hang = request.session.get('s_khach_hang')
        khach_hang = KhachHang.objects.get(id=s_khach_hang['id'])
        khach_hang.ho = ho
        khach_hang.ten = ten
        khach_hang.dien_thoai = dien_thoai
        khach_hang.dia_chi = dia_chi
        khach_hang.save()

        # Cập nhật vào session hiện tại (s_khach_hang)
        s_khach_hang['ho'] = ho
        s_khach_hang['ten'] = ten
        s_khach_hang['dien_thoai'] = dien_thoai
        s_khach_hang['dia_chi'] = dia_chi


    chuoi_kq_dmk = ''
    if request.POST.get('btnDoiMatKhau'):
        matkhau = request.POST.get('current_pwd')
        hasher = Argon2PasswordHasher()
        mk_encode = hasher.encode(matkhau, '12345678')

        s_khach_hang = request.session.get('s_khach_hang')
        id_kh = s_khach_hang['id']
        mk_khach_hang = KhachHang.objects.filter(id=id_kh, mat_khau=mk_encode)

        # Kiểm tra mật khẩu hiện tại
        if mk_khach_hang.count() > 0:
            # Kiểm tra mật khẩu mới có khớp với xác nhận mật khẩu
            mk_new = request.POST.get('new_pwd')
            mk_cf = request.POST.get('confirm_pwd')
            if mk_new != mk_cf:
                chuoi_kq_dmk = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Mật khẩu mới và Xác nhận Mật khẩu không giống nhau, vui lòng nhập lại!
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''
            else:
                mk_new_encode = hasher.encode(mk_new, '12345678')
                khach_hang = KhachHang.objects.get(id=id_kh)
                khach_hang.mat_khau = mk_new_encode
                khach_hang.save()
                s_khach_hang['mat_khau'] = mk_new_encode
                chuoi_kq_dmk = '''
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    Đổi mật khẩu thành công!
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''
        else:
            chuoi_kq_dmk = '''
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    Sai mật khẩu hiện tại, vui lòng kiểm tra lại!
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            '''

    return render(request, 'store/my-account.html', {
        'cart': cart,
        'chuoi_kq_dmk': chuoi_kq_dmk,
    })

