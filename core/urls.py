from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib import admin
from django.urls import path

@api_view(['GET'])
def hello_world(request):
        return Response({"message": "Hello, world!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hello_world,name="hello-world"),
]
