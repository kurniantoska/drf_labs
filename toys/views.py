from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

from toys.models import Toy
from toys.serializers import ToySerializer


class ToyGenericCBVList(generics.ListCreateAPIView):
    queryset = Toy.objects.all()
    serializer_class = ToySerializer
    

class ToyGenericCBVDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Toy.objects.all()
    serializer_class = ToySerializer
    

class ToyListMixin(mixins.ListModelMixin, 
                   mixins.CreateModelMixin,
                   generics.GenericAPIView):
    queryset = Toy.objects.all()
    serializer_class = ToySerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ToyDetailMixin(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     generics.GenericAPIView):
    queryset = Toy.objects.all()
    serializer_class = ToySerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ToyListCBV(APIView):
    """
    list all toys, or create a new toys
    """
    def get(self, request, format=None):
        toys = Toy.objects.all()
        serializer = ToySerializer(toys, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ToySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer, errors, status=status.HTTP_400_BAD_REQUEST)


class ToyDetailCBV(APIView):
    """
    Retrieve, update or delete a toy instance.
    """
    def get_object(self, pk):
        try:
            return Toy.objects.get(pk=pk)
        except Toy.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        toy = self.get_object(pk)
        serializer = ToySerializer(toy)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        toy = self.get_object(pk)
        serializer = ToySerializer(toy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        toy = self.get_object(pk)
        toy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
@api_view(['GET', 'POST'])
def toy_list(request):
    if request.method == 'GET':
        toys = Toy.objects.all()
        toys_serializer = ToySerializer(toys, many=True)
        return Response(toys_serializer.data)
    elif request.method == 'POST':
        # toy_data = JSONParser().parse(request)
        toys_serializer = ToySerializer(data=request.data)
        if toys_serializer.is_valid():
            toys_serializer.save()
            return Response(toys_serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(toys_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def toy_detail(request, pk):
    try:
        toy = Toy.objects.get(pk=pk)
    except Toy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        toy_serializer = ToySerializer(toy)
        return Response(toy_serializer.data)

    elif request.method == 'PUT':
        toy_serializer = ToySerializer(toy, data=request.data)
        if toy_serializer.is_valid():
            toy_serializer.save()
            return Response(toy_serializer.data)
        return Response(toy_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        toy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
