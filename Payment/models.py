from django.db import models
from django.db import models
from common.utils.validators import validator_phone_number


class Gateway(models.Model):
    title = models.CharField('title',max_length=30)
    description = models.TextField('description', blank=True)
    avatar = models.ImageField('avatar', blank=True, upload_to='gateways/')
    is_enable = models.BooleanField('is enable',default=True)
    created_time = models.DateTimeField('Time',auto_now_add=True)
    update_time = models.DateTimeField('Updatetime', auto_now_add=True)

    class Meta:
        db_table = 'gateways'
        verbose_name = 'Gateway'
        verbose_name_plural = 'Gateways'


class Payment(models.Model):
    STATUS_VOID = 0
    STATUS_PAID = 1
    STATUS_ERROR = 2
    STATUS_CANCELED = 3
    STATUS_REFOUNDED = 4
    STATUS_CHOICES = (
            (STATUS_VOID, "Void"),
            (STATUS_PAID, "Paid"),
            (STATUS_ERROR, "Error"),
            (STATUS_CANCELED, "User Canceled"),
            (STATUS_REFOUNDED, "Refounded")
    )


    user_id = models.ForeignKey('User.User', verbose_name= 'user', related_name='%(class)s', on_delete=models.CASCADE)
    gateway_id = models.ForeignKey('Gateway', verbose_name='gateway', related_name='%(class)s', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.PositiveSmallIntegerField('status', choices= STATUS_CHOICES, default= STATUS_VOID, db_index=True)
    device_uuid = models.CharField('device uuid', max_length=40, blank=True)
    token = models.CharField(max_length=200)
    phone_number = models.BigIntegerField('phone number', validators=[validator_phone_number], db_index=True)
    consumed_time = models.PositiveBigIntegerField('consumed reference code', null=True, db_index=True)
    created_time = models.DateTimeField('created time',auto_now_add=True, db_index=True)
    update_time = models.DateTimeField('modifaction time', auto_now_add=True)

    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'