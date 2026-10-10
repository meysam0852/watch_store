from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    """تمام مدل‌ها تاریخ ثبت و ویرایش دارند"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ آخرین ویرایش")

    class Meta:
        abstract = True


class SluggedMixinModel(models.Model):
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, verbose_name="نام")

    class Meta:
        abstract = True


class Brand(BaseModel):
    name = models.CharField(max_length=150, verbose_name="نام برند")
    meta_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="تایتل")
    meta_description = models.TextField(blank=True, null=True, verbose_name="دیسکریپشن")

    def __str__(self):
        return self.name


class Category(BaseModel, SluggedMixinModel):
    title = models.CharField(max_length=150, verbose_name="عنوان دسته‌بندی")

    def __str__(self):
        return self.title


class GenderChoices(models.TextChoices):
    MEN = 'men', 'مردانه'
    WOMEN = 'women', 'زنانه'
    UNISEX = 'unisex', 'اسپرت (یونیسکس)'

class EngineChoices(models.TextChoices):
    AUTOMATIC = 'automatic', 'اتوماتیک'
    QUARTZ = 'quartz', 'کوارتز'
    MECHANICAL = 'mechanical', 'مکانیکی کوکی'


class Product(BaseModel, SluggedMixinModel):
    title = models.CharField(max_length=255, verbose_name="عنوان محصول")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', verbose_name="برند")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="دسته‌بندی")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="قیمت")
    is_discount = models.BooleanField(default=False, verbose_name="تخفیف دارد؟")
    is_available = models.BooleanField(default=True, verbose_name="موجود در انبار؟")
    is_special = models.BooleanField(default=False, verbose_name="محصول ویژه؟")
    is_luxury = models.BooleanField(default=False, verbose_name="محصول لوکس؟")
    stash = models.PositiveIntegerField(default=0, verbose_name="موجودی انبار")
    click_count = models.PositiveIntegerField(default=0, verbose_name="تعداد بازدید")
    gender = models.CharField(max_length=10, choices=GenderChoices.choices, default=GenderChoices.UNISEX)
    origin = models.CharField(max_length=100, verbose_name="کشور سازنده")
    strap_matterial = models.CharField(max_length=100, verbose_name="جنس بند")
    usage = models.CharField(max_length=100, verbose_name="نوع کاربری")
    design = models.CharField(max_length=100, verbose_name="طراحی")
    engine = models.CharField(max_length=20, choices=EngineChoices.choices, default=EngineChoices.QUARTZ)
    main_image = models.ImageField(upload_to='products/main/', verbose_name="تصویر اصلی")
    features = models.JSONField(default=dict, blank=True, verbose_name="مشخصات فنی")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/gallery/')

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductColor(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color = models.CharField(max_length=50, verbose_name="نام رنگ")
    hex_code = models.CharField(max_length=7, verbose_name="کد رنگ")

    def __str__(self):
        return f"{self.color} ({self.product.title})"


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(max_length=15, unique=True, verbose_name="شماره تماس")

    def __str__(self):
        return f"{self.user.username} ({self.phone_number})"


class Comment(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(verbose_name="متن نظر")

    def __str__(self):
        return f"Comment by {self.customer.user.username} on {self.product.title}"


class WishList(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlists')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wished_products')
#در علاقه مندی ها دو دفعه ثبت نمی کنه محصول 
    class Meta:
        unique_together = ('customer', 'product')

    def __str__(self):
        return f"{self.customer.user.username} -> {self.product.title}"