from django.contrib import admin

from .models import PDFForHTML, PDFForURL


@admin.register(PDFForURL)
class PDFForURLAdmin(admin.ModelAdmin):

    pass


@admin.register(PDFForHTML)
class PDFForHTMLAdmin(admin.ModelAdmin):

    pass
