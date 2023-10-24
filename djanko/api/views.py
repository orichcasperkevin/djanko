import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status



# class StudentListManual(APIView):    
#     def get(self, request, pk=None):        
#         if not pk:
#             students = Student.objects.all()
#             serializer = StudentSerializer(students,many=True)
#             return Response(serializer.data,status =status.HTTP_200_OK)
           
#         student = Student.objects.get(id=pk)
#         serializer = StudentSerializer(student)
#         return Response(serializer.data,status =status.HTTP_200_OK)

class CurrentDateTime(APIView):
    def get(self,_):
        now = datetime.datetime.now()
        html = "<html><body>It is now %s.</body></html>" % now
        return Response(html,status=status.HTTP_200_OK)