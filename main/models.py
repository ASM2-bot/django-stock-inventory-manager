# main/models.py
from django.db import models

category_choice = (
    ('Furniture', 'Furniture'),
    ('IT Equipment', 'IT Equipment'),
    ('Phone', 'Phone'),
    ('ELECTRONICS', 'ELECTRONICS'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Stock(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    receive_quantity = models.IntegerField(default=0, blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default=0, blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default=0, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    Date = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=False)
    export_to_CSV = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Auto-assign category if missing
        if not self.category_id:
            default_category, created = Category.objects.get_or_create(
                name='General',
                defaults={'name': 'General'}
            )
            self.category = default_category
        
        # Ensure item_name is not empty
        if not self.item_name or self.item_name.strip() == '':
            self.item_name = 'Unnamed Item'
            
        super(Stock, self).save(*args, **kwargs)

    def __str__(self):
        return self.item_name or 'Unnamed Item'

    class Meta:
        verbose_name_plural = "Stock Items"
        ordering = ['-timestamp']