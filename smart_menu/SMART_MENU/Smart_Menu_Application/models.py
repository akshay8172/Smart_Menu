from django.db import models
from django.urls import reverse


class LoginTable(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20)
    
class RestaurantTable(models.Model):
    table_number = models.IntegerField(unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def __str__(self):
        return f"Table {self.table_number}"

    def get_absolute_url(self):
        return reverse('table_detail', kwargs={'table_number': self.table_number})


class DeliveryStaff(models.Model):
    LOGIN_ID = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone = models.BigIntegerField()
    email = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    photo = models.ImageField(upload_to='delivery_staff_images/') 
    
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    
class MenuItem(models.Model):
    CATEGORY_ID = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/')
    is_available = models.BooleanField(default=True)
    
class Offer(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='offers')
    offer_title = models.CharField(max_length=100)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.offer_title} ({self.discount_percentage}% off)"

    def get_discounted_price(self):
        return self.menu_item.price * (1 - self.discount_percentage / 100)

class Order(models.Model):
    TABLE = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE)
    order_time = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Changed from IntegerField
    status = models.CharField(max_length=20, default='Pending')
    is_active = models.BooleanField(default=True)
    
    
class OrderItem(models.Model):
    ORDER_ID = models.ForeignKey(Order, on_delete=models.CASCADE)
    MENU_ID = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    status = models.CharField(max_length=20,default='pending')

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} for Order {self.order.id}"
    
class Payment(models.Model):
    ORDER_ID = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)  # e.g., 'Credit Card', 'PayPal'
    status = models.CharField(max_length=20, default='Pending')  # e.g., 'Pending', 'Completed', 'Failed'
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"

class Assign(models.Model):
    STAFF = models.ForeignKey(DeliveryStaff,on_delete=models.CASCADE)
    ORDER = models.ForeignKey(Order,on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='assigned')

    
class Feedback(models.Model):
    ORDER = models.ForeignKey(Order,on_delete=models.CASCADE)
    feedback = models.TextField()
    ratings = models.IntegerField()
    TABLE = models.ForeignKey(RestaurantTable, on_delete=models.CASCADE)
