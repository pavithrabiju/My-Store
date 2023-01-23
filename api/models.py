from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here



class Products(models.Model):
    name = models.CharField( max_length=200)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    image = models.ImageField(null=True,upload_to="images")

#avg_rating
    @property
    def avg_rating(self):
        ratings=self.reviews_set.all().values_list("rating",flat=True)
        if ratings:
            return sum(ratings)/len(ratings)
        else:
            return 0


    def review_user(self):
        ratings=self.reviews_set.all().values_list("rating",flat=True)
        if ratings:
            return len(ratings)
        else:
            return 0

    def __str__(self):
        return self.name


class carts(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

class Reviews(models.Model):
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=200)

    def __str__(self):
        return self.comment




#ORM
#orm for creating a resource
#model.name.objects.create(field1=value1,field2=value2,,,)
#products.objects.create(name="samsung72",price=32000,description="mobile",category="electronics")

#ORM query for fetching all records
#qs=modelname.object.all()

#ORM filter queries
#qs=modelname.objects.filter(category="electronics")
#qs=Products.objects.all().exclude(category="electronics")

#om query for fetching a specific record
#qs=modelname.objects.get(id=1)

#price>2500
#qs=Products.objects.filter(price__lt=2500)
#products in range of 20000 to 30000
#return all categories
#products.objects.values_list(category)













