import boto3
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Image
from .serializers import ImageSerializer

class ImageUploadView(APIView):
    def post(self, request, format=None):
        file_obj = request.FILES.get('image')
        if not file_obj:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)

        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        object_name = file_obj.name

        try:
            # Uploading file object to S3
            s3_client.upload_fileobj(file_obj, bucket_name, object_name)
            s3_url = f"https://{bucket_name}.s3.amazonaws.com/{object_name}"
            
            # Save metadata to DB
            image_instance = Image.objects.create(name=object_name, s3_url=s3_url)
            serializer = ImageSerializer(image_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
