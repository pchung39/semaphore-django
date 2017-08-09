from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .signup_form import UserCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from .serializers import *
from datetime import datetime
import jwt

#JWT secret key
SECRET_KEY = "bananas"

'''
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')
'''
'''
        jwt.decode(encoded, 'secret', algorithms=['HS256'])
'''


def lander(request):
    return render(request, 'index.html')

# posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
@api_view(['POST'])
def signin(request):
    if request.method == 'POST':
        signin_form = UserSerializer()
        response = signin_form.signin(request.data)
        token = jwt.encode({'id': response["user_id"]}, SECRET_KEY, algorithm='HS256')
        return JsonResponse({"token": token.decode("utf-8")}, status=status.HTTP_200_OK)

@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        signup_form = UserSerializer()
        response = signup_form.create(request.data)
        token = jwt.encode({'id': response["user_id"]}, SECRET_KEY, algorithm='HS256')
        return JsonResponse({"token": token.decode("utf-8")}, status=status.HTTP_200_OK)

'''
@login_required(login_url='/signin/')
def manage_services(request):

    aws_instances = Instance.objects.filter(user_id=request.user.id, instance_provider='Amazon Web Services').values()
    gcp_instances = Instance.objects.filter(user_id=request.user.id, instance_provider='Google Cloud Platform').values()
    azure_instances = Instance.objects.filter(user_id=request.user.id, instance_provider='Microsoft Azure').values()
    return render(request, 'manage.html', { 'aws': aws_instances, 'gcp': gcp_instances, 'azure': azure_instances })


def delete_instance(request, instance_id):

    query = Instance.objects.filter(id=instance_id)
    query.delete()
    return redirect('manage')
'''
# TODO: make adding a hostname a pop up instead of a page

@login_required(login_url='/signin/')
def select_service(request):
    if request.method == 'POST':
        instance_form = request.POST['instance']
        instance_provider_form = request.POST['instance_provider']
        provider_service_form = request.POST['provider_service']

        new_instance = Instance(user_id=request.user.id, instance=instance_form, instance_provider=instance_provider_form, provider_service=provider_service_form)
        new_instance.save()


        if new_instance.pk is None:
            message.error(request, 'There was an error')
        else:
            instance_added = "'%s' has been added" % instance_form
            return redirect('manage')

    else:
        return render(request, 'manage.html')

def logout(request):
    logout(request)
    return render(request, 'index.html')


# GET INSTANCE
@api_view(['GET', 'DELETE', 'PUT'])
def get_put_delete_instance(request, instance_id):

    try:
        instance = Instance.objects.get(user_id=request.user.id, pk=instance_id)
    except Instance.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InstanceSerializer(instance)
        return Response(serializer.data)

    if request.method == 'DELETE':
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    if request.method == 'PUT':
        serializer = InstanceSerializer(puppy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# GET ALL INSTANCES
@api_view(['GET', 'POST'])
def get_all_or_post_instances(request):
    #check request header
    #if request.META['HTTP_AUTHORIZATION']:
        #user_id = request.META['HTTP_AUTHORIZATION']
        #jwt.decode(encoded, SECRET, algorithms=['HS256'])
    #else:
    #user_id = request.POST['user_id']
    user_id = request.META.get('HTTP_AUTHORIZATION')
    if request.method == 'POST':
        try:
            instance_serializer = InstanceSerializer()
            instance = instance_serializer.save(request.data, user_id)
            return Response(instance, status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            instances = Instance.objects.filter(user_id=user_id)
            serializer = InstanceSerializer(instances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Instance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def post_pingresults(request, instance_id):
    user_id = request.META.get('HTTP_AUTHORIZATION')
    print(user_id)
    try:
        ping_serializer = PingResultsSerializer()
        post_ping = ping_serializer.save(request.data, user_id, instance_id)
        return Response(post_ping, status=status.HTTP_200_OK)
    except:
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
