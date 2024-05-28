from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

class UserAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def get(self, request, id=None):
        if id:
            user = User.objects.filter(id=id).first()
            if user:
                serializer = UserSerializer(user)
                return Response(serializer.data)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        if not id:
            return Response({"error": "Method PUT not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = User.objects.filter(id=id).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not id:
            return Response({"error": "Method DELETE not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = User.objects.filter(id=id).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def put(self, request, id=None):
        if not id:
            return Response({"error": "Method PUT not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        user = User.objects.filter(id=id).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=True)  # Allow partial update
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
