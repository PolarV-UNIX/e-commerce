from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


"""CATEGORY MPDEL"""
class Category(models.Model):
    parrent = models.ForeignKey('self', verbose_name='parrent', blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField('name', blank=True, null=True, max_length=50, unique=True)
    image = models.ImageField('icon', blank=True, null=True, upload_to='media/')
    is_enable = models.BooleanField('is_enable', default=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    modify_at = models.DateTimeField('modify_at', auto_now=True)


    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    
"""PRODUCT MODEL"""
class Product(models.Model):
    title = models.CharField('title', max_length=50, blank=True, null=True)
    categories = models.ManyToManyField('Product.Category', related_name="category_by",verbose_name='category', blank=True)
    image_id = models.ForeignKey('Product.ImageProduct', verbose_name='image', null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField('price', max_digits=6, decimal_places=2, default=0)
    discription = models.CharField('discription', max_length=400, blank=True, null=True)
    is_enable = models.BooleanField('is_enable', default=True)
    duration = models.DurationField('duration', blank=True, null=True)
    discount = models.IntegerField('discount', default=0)
    created_by = models.ForeignKey('User.User', verbose_name='created_by', on_delete=models.SET_NULL, editable=False, blank=True, null=True)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    modify_at = models.DateTimeField('modify_at', auto_now=True)
    rate = models.DecimalField(max_digits=6, decimal_places=1, null=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

"""IMAGE PRODUCT MODEL"""
class ImageProduct(models.Model):
    product_id = models.ForeignKey('Product', verbose_name='product', default=None, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField('image', blank=True, null=True, upload_to='media/')
    is_main = models.BooleanField('main', default=False, null=True, blank=True, help_text='Active To Publish MAIN Image')
    is_active = models.BooleanField('is_active', default=False)
    created_at = models.DateTimeField('created_at', auto_now_add=True)
    modify_at = models.DateTimeField('modify_at', auto_now=True)

    class Meta:
        db_table = 'imagesproduct'
        verbose_name = 'ImageProduct'
        verbose_name_plural = 'ImagesProduct'
        
""" RATING MODEL """
class Rating(models.Model):
    rate = models.DecimalField(max_digits=6, decimal_places=1, null=True)
    user_id = models.ForeignKey("User.User", on_delete=models.SET_NULL, null=True)
    product_id = models.ForeignKey('Product', null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'rating'
        verbose_name = 'rate_point'
        verbose_name_plural = 'rates_points'