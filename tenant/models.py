from django.db import models
from account.models import User
from django_tenants.models import DomainMixin, TenantMixin


class Tenant(TenantMixin):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    instituteName = models.CharField(max_length=100)
    ownerName=models.CharField(max_length=100)
    address =models.TextField()
    pinCode = models.PositiveIntegerField(null =True)
    city = models.CharField(max_length=100,null =True)
    state=models.CharField(max_length=100,null =True)
    contactNo=models.PositiveBigIntegerField(null =True)
    emailId=models.EmailField(null=True)
    allowed_until = models.DateField(null=True)
    on_trial = models.BooleanField(null =True)

    is_active = models.BooleanField(default=False, blank=True)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and
    # synced when it is saved
    auto_create_schema = True

    """
    USE THIS WITH CAUTION!
    Set this flag to true on a parent class if you want the schema to be
    automatically deleted if the tenant row gets deleted.
    """
    auto_drop_schema = True


    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return f"{self.instituteName}"


class Domain(DomainMixin):
    pass