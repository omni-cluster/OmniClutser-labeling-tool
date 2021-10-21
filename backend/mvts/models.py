from django.db import models

# Create your models here.
class User_file(models.Model):
    file_name = models.CharField(max_length=40, primary_key=True)
    file_content = models.TextField(null=False)
    file_label = models.IntegerField()

class File_template(models.Model):
    file_label = models.IntegerField(primary_key=True)
    file_name = models.CharField(max_length=40)

