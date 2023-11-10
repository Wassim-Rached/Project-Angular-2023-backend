from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from accounts.models import Account
from activities.models import Activity


import logging


class AccountPhotoView(APIView):
    def get(self, request, pk):
        try:
            instance = Account.objects.get(pk=pk)
            image_path = instance.photo.path
            logging.info(f"Image path: {image_path}")
            return FileResponse(open(image_path, "rb"))
        except Account.DoesNotExist:
            logging.error(f"Account with pk={pk} does not exist.")
            return Response({"error": "Account not found"}, status=404)
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return Response({"error": "An error occurred"}, status=500)


class ActivityPhotoView(APIView):
    def get(self, request, pk):
        try:
            instance = Activity.objects.get(pk=pk)
            image_path = instance.photo.path
            return FileResponse(open(image_path, "rb"))
        except Account.DoesNotExist:
            return Response({"error": "MyModel not found"}, status=404)
