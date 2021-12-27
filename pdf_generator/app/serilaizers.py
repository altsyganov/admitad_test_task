from rest_framework import serializers

from .models import PDFForURL, PDFForHTML


class PDFSerializerBase:

    pdf = serializers.SerializerMethodField('get_pdf_url')

    def get_pdf_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.pdf.url)


class PDFForUrlSerializer(serializers.ModelSerializer, PDFSerializerBase):

    url = serializers.URLField(source='requested_url')

    class Meta:
        model = PDFForURL
        fields = ('pdf', 'url')


class PDFForHTMLSerializer(serializers.ModelSerializer, PDFSerializerBase):

    html = serializers.FileField(source='requested_html')

    class Meta:
        model = PDFForHTML
        fields = ('pdf', 'html')

    def validate_html(self, value):
        if value.name.endswith('.html'):
            return value
        raise serializers.ValidationError('provide html file')
