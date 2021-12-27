from django.shortcuts import resolve_url
from celery.result import AsyncResult
from rest_framework.viewsets import GenericViewSet
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import PDFForHTML, PDFForURL
from .serilaizers import PDFForUrlSerializer, PDFForHTMLSerializer
from .tasks import generate_pdf_from_html, generate_pdf_from_url


class PDFActions(GenericViewSet):

    @staticmethod
    def __result(serialized_instance):
        if serialized_instance.data['pdf']:
            return Response(status=200, data=serialized_instance.data)
        elif serialized_instance.data.get('task_id'):
            task = AsyncResult(serialized_instance.data['task_id'])
            if task.status == 'FAILURE':
                return Response(status=500, data={'text': task.result})
            else:
                return Response(status=425, data={'text': 'Task is still running. Try later.'})
        else:
            return Response(status=425, data={'text': 'Task is still running. Try later.'})

    @action(methods=['POST'], detail=False)
    def pdf_for_url(self, request):
        serializer = PDFForUrlSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            generate_pdf_from_url.delay(instance.id)
            url = request.build_absolute_uri(resolve_url('pdf-actions-result-from-url', pk=instance.id))
            data = {
                'result': url
            }
            return Response(status=202, data=data)

    @action(methods=['POST'], detail=False, parser_classes=(MultiPartParser, ))
    def pdf_for_file(self, request):
        serializer = PDFForHTMLSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            generate_pdf_from_html.delay(instance.id)
            url = request.build_absolute_uri(resolve_url('pdf-actions-result-from-file', pk=instance.id))
            data = {
                'result': url
            }
            return Response(status=202, data=data)

    @action(methods=['GET'], detail=True, name='result-from-file')
    def result_from_file(self, request, pk):
        obj = PDFForHTML.objects.get(pk=pk)
        serializer = PDFForHTMLSerializer(instance=obj, context={'request': request})
        return self.__result(serializer)

    @action(methods=['GET'], detail=True, name='result-from-url')
    def result_from_url(self, request, pk):
        obj = PDFForURL.objects.get(pk=pk)
        serializer = PDFForUrlSerializer(instance=obj, context={'request': request})
        return self.__result(serializer)
