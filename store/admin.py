from django.contrib import admin
from store.models import *
from datetime import datetime
from django.utils.html import format_html

# Register your models here.

def change_public_day(modeladmin, request, queryset):
    queryset.update(public_day=datetime.now())

change_public_day.short_description = 'Change public_day to Today'

class ProductAdmin(admin.ModelAdmin):
    # loại trừ các thuộc tính trên trang thêm/cập nhật
    exclude = ('public_day', 'viewed')

    # Hiển thị ra danh sách các cột
    # list_display = ('name', 'price', 'public_day', 'viewed')
    list_display = ('change_column_name', 'change_column_price', 'change_column_public_day', 'change_column_viewed', 'change_column_image')

    # Lọc
    list_filter = ('public_day',)

    # tìm kiếm
    search_fields = ('name__contains',)

    # Sắp xếp
    ordering = ('-viewed',)

    # Action
    actions = [change_public_day]

    # Đổi tên cột, gán tên hàm lên phần hiển thị ở trên
    @admin.display(description="Tên sản phẩm")
    def change_column_name(self, obj):
        return '%s' %obj.name

    @admin.display(description="Giá")
    def change_column_price(self, obj):
        return '%s' %"{:,}".format(int(obj.price))  # "{:,}".format(obj.price) : chuyển chuỗi thành tiền tệ
    
    @admin.display(description="Ngày sản xuất")
    def change_column_public_day(self, obj):
        return '%s' %obj.public_day
    
    @admin.display(description="Lượt xem")
    def change_column_viewed(self, obj):
        return '%s' %obj.viewed

    @admin.display(description="Hình ảnh")
    def change_column_image(self, obj):
        return format_html('<img src="%s" alt="%s" style="width: 45px; height: 45px;" >' %(obj.image.url, obj.name) )

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product, ProductAdmin)

admin.site.site_header = 'EStore Administrator'


