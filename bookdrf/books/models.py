from django.db import models

class Books(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=400, null=True, blank=True)
    author = models.CharField(max_length=150)
    published_data = models.DateField()
    views = models.PositiveIntegerField(default=0)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Book"

    def __str__(self):
        return self.title
    

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name