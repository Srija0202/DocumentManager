from django.db import models
import textract
import os

# Create your models here.
class Document(models.Model):
    name = models.CharField(max_length=255)
    document = models.FileField()
    document_type = models.ForeignKey("DocumentType",on_delete=models.CASCADE)
    ocr_data = models.TextField(blank=True)

    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        super(Document, self).save(*args, **kwargs)
        Document.objects.filter(pk=self.pk).update(ocr_data = textract.process(self.document.path).decode('utf-8'))
        
         



class DocumentType(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name