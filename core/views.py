from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def hello_world(request):
    return Response({"message": "Hello, world!"})


def healthcheck_view(request):
    return Response(status=200)
