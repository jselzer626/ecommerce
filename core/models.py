from django.db import models
from django.conf import settings
from django.urls import reverse
from django.db.models import Sum

# Create your models here.
class Item(models.Model):
    
    name = models.CharField(max_length=25)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, blank=True, through='OrderDetail')
    completed = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def updateTotal(self):
        order_items = OrderDetail.objects.filter(order = self.id).all()
        self.total = order_items.aggregate(Sum('total'))['total__sum'] if len(order_items) > 0 else 0.0
        self.save()
        return self.total
    
    def __str__(self):
        return f"Order #{self.id} Total: {self.total}"

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def updateTotal(self):
        self.total = self.item.priceLarge * self.quantity if self.size == 'LG' else self.item.priceSmall * self.quantity
        self.save()
        return self.total
    
    def __str__(self):
        self.updateTotal()
        return f"{self.item} {self.size} X {self.quantity} - ${self.total}"