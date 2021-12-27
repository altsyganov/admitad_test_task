from uuid import uuid4

from django.db import models


class TimeStampedModel(models.Model):

    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PDFRequestBase(TimeStampedModel):

    class Meta:
        abstract = True

    task_id = models.UUIDField(null=True)
    pdf = models.FileField(null=True, upload_to='pdfs/')


class PDFForHTML(PDFRequestBase):

    requested_html = models.FileField(upload_to='htmls/')


class PDFForURL(PDFRequestBase):

    requested_url = models.URLField()
