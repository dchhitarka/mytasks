from rest_framework import status
from rest_framework.exceptions import ValidationError
# from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .models import *
from .serializers import *
import json

# Create your views here.
@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def tasks(request):
    if request.method == 'GET':
        data = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        if not 'title' in data.keys():
            return Response({'detail':'No task name found.'}, status=status.HTTP_404_NOT_FOUND)
        data["user"] = request.user.id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE', 'PUT'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def items(request, task_id):
    task = Task.objects.filter(pk=task_id)
    if task:
        if task[0].user == request.user:
            if request.method == 'GET':
                data = Item.objects.filter(task=task[0])
                serializer = ItemSerializer(data, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        
            elif request.method == 'POST':
                data = json.loads(request.body.decode("utf-8"))
                if not 'title' in data.keys():
                    return Response({'detail':'No item name found.'}, status=status.HTTP_404_NOT_FOUND)
                data["task"] = task_id
                serializer = ItemSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            elif request.method == 'DELETE':
                task[0].delete()
                return Response('Task deleted', status=status.HTTP_200_OK)

            elif request.method == 'PUT':
                data = json.loads(request.body.decode("utf-8"))
                if 'title' in data.keys():
                    task[0].title = data["title"]
                task[0].save()
                return Response('Task updated', status=status.HTTP_200_OK)
    
        return Response('Not authorized', status=status.HTTP_401_UNAUTHORIZED)        
    
    return Response('Task not found', status=status.HTTP_404_NOT_FOUND)
    
@api_view(['DELETE', 'PUT'])
@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def item(request, task_id, item_id):
    item = Item.objects.filter(pk=item_id)
    task = Task.objects.get(pk=task_id)
    if item:
        print(item[0].task)
        if item[0].task == task:
            if request.method == 'DELETE':
                item[0].delete()
                return Response('Item deleted', status=status.HTTP_200_OK)

            elif request.method == 'PUT':
                data = json.loads(request.body.decode("utf-8"))
                if 'title' in data.keys():
                    item[0].title = data["title"]
                if 'status' in data.keys():
                    item[0].status = data["status"]
                item[0].save()
                return Response('Item updated', status=status.HTTP_200_OK)
    
        return Response('Not authorized', status=status.HTTP_401_UNAUTHORIZED)        
    
    return Response('Task not found', status=status.HTTP_404_NOT_FOUND)
    

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    try:
        data = {}
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            account.is_active = True
            account.save()
            token = Token.objects.get_or_create(user=account)[0].key
            data["message"] = "User registered successfully"
            data["email"] = account.email
            data["username"] = account.username
            data["token"] = token
        else:
            data = serializer.errors
        return Response(data)
    except BaseException as e:
        account=User.objects.get(username='')
        account.delete()
        raise ValidationError({"400": f'{str(e)}'})

    except KeyError as e:
        print(e)
        raise ValidationError({"400": f'Field {str(e)} missing'})

@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
        data = {}
        reqBody = json.loads(request.body.decode("utf-8"))
        print(reqBody)
        email = reqBody['email']
        password = reqBody['password']
        try:
            Account = User.objects.get(email=email)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})
        token = Token.objects.get_or_create(user=Account)[0].key
        print(Account.password)
        if not Account.check_password(password):
            raise ValidationError({"message": "Incorrect Login credentials"})
        if Account:
            if Account.is_active:
                print(request.user)
                login(request, Account)
                data["message"] = "user logged in"
                data["email"] = Account.email
                data["id"] = Account.id
                data["username"] = Account.username
                Res = {"data": data, "token": token}
                return Response(Res)
            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    logout(request)
    return Response('User Logged out successfully')