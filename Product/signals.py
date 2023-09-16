from django.db.models.signals import post_save
from django.dispatch import receiver
from Product.models import Rating, Product
from django.db.models import Avg


@receiver(post_save, sender=Rating)
def update_product_avg_rating(sender, instance, **kwargs):
    product = instance.product_id
    avg_rating = Rating.objects.filter(product_id=product).aggregate(avg_rating=Avg('rate'))['avg_rating']
    product.rate = avg_rating
    product.save()