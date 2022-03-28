from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
#from rest_framework import permissions
from .models import GithubProject
from .serializers import GithubProjectSerializer

class ProjectViews(APIView):
    def post(self, request):
        serializer = GithubProjectSerializer(data=request.data)
        if serializer.is_valid():
            print("FOOBARRRRRR")
            print(self.request.user)
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):
        if id:
            try:
                item = GithubProject.objects.get(id=id)
                serializer = GithubProjectSerializer(item)
                return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
            except:
                return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        items = GithubProject.objects.all()
        serializer = GithubProjectSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, id):
        try:
            item = GithubProject.objects.get(id=id)
            data = {
                'name': request.data.get('name'), 
                'description': request.data.get('description'), 
                'link': request.data.get('link'),
                'rating': request.data.get('rating'),
            }
            serializer = GithubProjectSerializer(instance = item, data=data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        try:
            item = GithubProject.objects.get(id=id)
            item.delete()
            return Response(
                {"res": "Object deleted!"},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {"res": "Object with id does not exists"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
