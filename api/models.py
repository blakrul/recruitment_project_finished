from django.db import models


class Car(models.Model):
    make = models.CharField(max_length=36)
    model = models.CharField(max_length=36)

    @property
    def avg_rating(self):
        from decimal import Decimal
        if self.id:
            rating_db = Rating.objects.filter(car_id=self.id)
            rates_number = Rating.objects.filter(car_id=self.id).count()
            rates_sum = sum(z.rating for z in rating_db)
            if not rates_sum and not rates_number:
                return '0'
            avg_number = rates_sum / rates_number
            return Decimal(avg_number).quantize(Decimal('.1'))

        return '0'

    @property
    def rates_number(self):
        if self.id:
            return Rating.objects.filter(car_id=self.id).count()
        return '0'

    def __str__(self):
        return '%s %s' % (self.make, self.model)

    class Meta:
        verbose_name_plural = "Cars"


class Rating(models.Model):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
