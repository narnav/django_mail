# from django.http import HttpResponse
# from django.views import View
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import serializers
from django.contrib.auth.models import User
from .serializers import TaskSerializer
from .models import Task


from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
# //////////// image upload / display
# return all images to client
from .models import MPrint
from django.core.mail import get_connection, send_mail
from django.conf import settings

# def send_mail(
#     subject: str,
#     message: str,
#     from_email: str | None,
#     recipient_list: List[str],
#     fail_silently: bool = ...,
#     auth_user: str | None = ...,
#     auth_password: str | None = ...,
#     connection: Any | None = ...,
#     html_message: str | None = ...
# ) -> int

msg =    """Hello Eyal Goldestain,

Microsoft LTD.
Herzliya Pituach, Hamovil 4
Israel

Dear Amir,

I am thrilled to extend my warmest congratulations and formally welcome you to the Microsoft family! We are excited that you have accepted the offer for the C# Programmer position at our offices. Your enthusiasm and expertise will undoubtedly contribute to our ongoing mission of innovation and technological excellence.

Your decision to join Microsoft LTD is a testament to your dedication and skill in C# programming, and we are confident that your contributions will play a pivotal role in our continued success. Our commitment to fostering a collaborative work environment and cutting-edge technologies aligns perfectly with your aspirations, and we are eager to witness the positive impact you will have on our projects.

Your proficiency in C# programming, coupled with your proven experience in software development and problem-solving, aligns well with the challenges and opportunities that lie ahead. We believe your presence will further elevate the capabilities of our talented team, and we are excited about the knowledge sharing and growth that will result from your involvement.

We sincerely appreciate the trust you have placed in Microsoft LTD, and we are fully committed to supporting your journey as a C# Programmer within our esteemed organization. The values and goals that define our company will be upheld with your contributions, and we look forward to achieving mutual success together.

Regarding the onboarding process, our HR department will be in touch shortly to provide you with all necessary paperwork, orientation details, and training schedules. Your willingness to facilitate a smooth transition is greatly appreciated, and we are here to assist you every step of the way.

In terms of compensation, I'm pleased to confirm that your monthly salary will be 32,000 NIS.

Once again, welcome to Microsoft LTD, Amir. Your dedication and commitment are highly valued, and we are excited to embark on this journey of growth and innovation with you.

Warm regards,

Eyal Goldstein
C# DEVELOPER - outsource developer
Microsoft LTD
 """



@api_view(['GET'])
def send(request):
    connection = get_connection()
    connection.open()
    send_mail(
    "open programer position",
    msg,
    "Amir_dagan@Microsoft.co.il",
    ["narnavg@gmail.com"],
    fail_silently=False,
    )
    connection.close()
    return Response("email sent")



@api_view(['GET'])
def getTasks(request):
    res = []  # create an empty list
    for img in Task.objects.all():  # run on every row in the table...
        res.append({"title": img.title,
                    "description": img.description,
                    "completed": False,
                    "image": str(img.image)
                    })  # append row by to row to res list
    return Response(res)  # return array as json response

# upload image method (post)


class ImageUpload(APIView):
    parser_class = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        api_serializer = TaskSerializer(data=request.data)

        if api_serializer.is_valid():
            api_serializer.save()
            return Response(api_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', api_serializer.errors)
            return Response(api_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        pass
# //////////// end      image upload / display


@permission_classes([IsAuthenticated])
class MyModelView(APIView):
    """
    This class handle the CRUD operations for MyModel
    """

    def get(self, request):
        """
        Handle GET requests to return a list of MyModel objects
        """
        my_model = Task.objects.all()
        serializer = TaskSerializer(my_model, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Handle POST requests to create a new Task object
        """
        # usr =request.user
        # print(usr)
        serializer = TaskSerializer(
            data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        Handle PUT requests to update an existing Task object
        """
        my_model = Task.objects.get(pk=pk)
        serializer = TaskSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Handle DELETE requests to delete a Task object
        """
        my_model = Task.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ////////////////////////////////login /register
# login
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        # ...
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# register


@api_view(['POST'])
def register(req):
    username = req.data["username"]
    password = req.data["password"]
    # create a new user (encrypt password)
    try:
        User.objects.create_user(username=username, password=password)
    except:
        return Response("error")
    return Response(f"{username} registered")


# ///////////////////////////end login

# //////////test method
@api_view(['GET'])
def test(req):
    return Response("hello")

# /////////// Tasks table (CRUD)


@api_view(['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def tasks(req, id=-1):
    if req.method == 'GET':
        user = req.user
        if id > -1:
            try:
                temp_task = user.task_set.get(id=id)
                return Response(TaskSerializer(temp_task, many=False).data)
            except Task.DoesNotExist:
                return Response("not found")

        all_tasks = TaskSerializer(user.task_set.all(), many=True).data
        return Response(all_tasks)

    if req.method == 'POST':
        print(type(req.user))
        Task.objects.create(
            title=req.data["title"], description=req.data["description"], completed=req.data["completed"], user=req.user)
        return Response("post...")

    if req.method == 'DELETE':
        user = req.user
        try:
            temp_task = user.task_set.get(id=id)
        except Task.DoesNotExist:
            return Response("not found")

        temp_task.delete()
        return Response("del...")
    if req.method == 'PUT':
        user = req.user
        try:
            temp_task = user.task_set.get(id=id)
        except Task.DoesNotExist:
            return Response("not found")

        old_task = user.task_set.get(id=id)
        old_task.title = req.data["title"]
        old_task.completed = req.data["completed"]
        old_task.description = req.data["description"]
        old_task.save()
        return Response("res")


class MPrintSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPrint
        fields = '__all__'

    def create(self, validated_data):
        # user = self.context['user']
        # print(user)
        return MPrint.objects.create(**validated_data)  # , user=user)
   # model crud
# @permission_classes([IsAuthenticated])


class MPrintView(APIView):
    def get(self, request):
        # my_model = request.user.task_set.all()
        my_model = MPrint.objects.all()
        serializer = MPrintSerializer(my_model, many=True)
        return Response(serializer.data)

    def post(self, request):
        # usr =request.user
        # print(usr)
        serializer = MPrintSerializer(
            data=request.data)  # , context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        my_model = MPrint.objects.get(pk=pk)
        serializer = MPrintSerializer(my_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        my_model = MPrint.objects.get(pk=pk)
        my_model.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    #     user =models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    # title = models.CharField(max_length=50)
    # description = models.CharField(max_length=100)
    # completed = models.BooleanField(default=False)
        # req.data["user_id"] = "eyal" # req.user

        # tsk_serializer = TaskSerializer(data=req.data)

        # if tsk_serializer.is_valid():
        #     tsk_serializer.save()
