from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from accounts.models import Account
from activities.models import Activity


class AccountPhotoView(APIView):
    def get(self, request, pk):
        try:
            instance = Account.objects.get(pk=pk)
            image_path = instance.photo.path
            return FileResponse(open(image_path, "rb"))
        except Account.DoesNotExist:
            return Response({"error": "MyModel not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class ActivityPhotoView(APIView):
    def get(self, request, pk):
        try:
            instance = Activity.objects.get(pk=pk)
            image_path = instance.photo.path
            return FileResponse(open(image_path, "rb"))
        except Account.DoesNotExist:
            return Response({"error": "MyModel not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
