from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from djangoratings.fields import RatingField
from djangoratings.fields import AnonymousRatingField



"""CATEGORY MPDEL"""
class Category(models.Model):
    parrent = models.ForeignKey('self', verbose_name='parrent', blank=True, null=True, on_delete=models.SET_NULL)
    product = models.ManyToManyField('Product', verbose_name='product', blank=True, null=True)
    name = models.CharField('name', blank=True, null=True, max_length=50, unique=True)
    image = models.ImageField('icon', blank=True, null=True, upload_to='media/')
    is_enable = models.BooleanField('is_enable', default=True)
    created_time = models.DateTimeField('created_time', auto_now_add=True, null=True, blank=True)
    modify_date = models.DateTimeField('modify_date', auto_now=True, null=True, blank=True)


    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title
    
"""PRODUCT MODEL"""
class Product(models.Model):
    title = models.CharField('title', max_length=50, blank=True, null=True),
    category = models.ManyToManyField('Category', verbose_name='category', null=True, blank=True)
    image = models.ForeignKey('ImageProduct', verbose_name='image', null=True, blank=True, on_delete=models.SET_NULL)
    price = models.DecimalField('price', max_digits=900, decimal_places=1, default=0)
    discription = models.CharField('discription', max_length=400, blank=True, null=True)
    short_discription = CKEditor5Field('short_discription', config_name='extends',blank=True, null=True, default=None)
    is_enable = models.BooleanField('is_enable', default=True)
    duration = models.DurationField('duration', blank=True, null=True)
    discount = models.IntegerField('discount', default=0)
    created_by = models.ForeignKey('User', verbose_name='created_by', on_delete=models.SET_NULL, editable=False, blank=True, null=True)
    created_time = models.DateTimeField('created_time', auto_now_add=True)
    modify_date = models.DateTimeField('modify_date', auto_now=True, auto_now_add=True)
    rating = RatingField(range=5, can_change_vote= True, allow_delete=True, use_cookies=True)
    ratinganonymos = AnonymousRatingField(range=5, allow_anonymos=True)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

"""IMAGE PRODUCT MODEL"""
class ImageProduct(models.Model):
    product = models.ForeignKey('Product', verbose_name='product', default=None, null=True, blank=True, on_delete=models.SET_NULL)
    image = models.ImageField('image', blank=True, null=True, upload_to='media/')
    is_main = models.BooleanField('main', default=False, null=True, blank=True, help_text='Active To Publish MAIN Image')
    is_active = models.BooleanField('is_active', default=False)
    created_time = models.DateTimeField('created_time', auto_now_add=True, auto_now=False)
    modify_date = models.DateTimeField('modify_date', auto_now=True, auto_now_add=True)

    class Meta:
        db_table = 'imagesproduct'
        verbose_name = 'ImageProduct'
        verbose_name_plural = 'ImagesProduct'