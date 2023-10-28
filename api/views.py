from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from accounts.models import Account


class AccountPhotoView(APIView):
    def get(self, request, pk):
        try:
            my_model = Account.objects.get(pk=pk)
            image_path = my_model.photo.path
            return FileResponse(open(image_path, "rb"))
        except Account.DoesNotExist:
            return Response({"error": "MyModel not found"}, status=404)
