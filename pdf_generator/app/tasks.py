import pdfkit
from pdf_generator.celery import app
from django.core.files.base import ContentFile


from .models import PDFForHTML, PDFForURL


@app.task()
def generate_pdf_from_html(html_request_id):
    obj = PDFForHTML.objects.get(pk=html_request_id)
    response = pdfkit.from_file(obj.requested_html.path, False, verbose=True)
    file = ContentFile(response, name=f'{generate_pdf_from_html.request.id}.pdf')
    obj.pdf = file
    obj.task_id = generate_pdf_from_html.request.id
    obj.save()
    data = {
        'model': obj._meta.model_name,
        'id': obj.id
    }
    return data


@app.task()
def generate_pdf_from_url(url_request_id):
    obj = PDFForURL.objects.get(pk=url_request_id)
    response = pdfkit.from_url(obj.requested_url, False)
    file = ContentFile(response, name=f'{generate_pdf_from_url.request.id}.pdf')
    obj.pdf = file
    obj.task_id = generate_pdf_from_url.request.id
    obj.save()
    data = {
        'model': obj._meta.model_name,
        'id': obj.id
    }
    return data
