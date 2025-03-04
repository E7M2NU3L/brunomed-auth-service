from rest_framework.views import APIView
from rest_framework.response import Response

class Health(APIView):
    def post(self, request, format=None):
        context = {
            'status': True,
            'message': "App is working fine, POST request is completed",
            'method': 'POST'
        }
        return Response(context)

    def get(self, request, format=None):
        context = {
            'status': True,
            'message': "App is working fine",
            'method': 'GET'
        }
        return Response(context) 
