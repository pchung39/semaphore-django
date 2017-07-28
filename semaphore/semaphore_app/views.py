from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .signup_form import UserCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
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
        form = UserSerializer()
        response = form.signin(request.data)
        token = jwt.encode({'id': response.user_id)}, SECRET_KEY, algorithm='HS256')
        token_object = {"token": token}


@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        signup_form = UserSerializer()
        response = signup_form.create(request.data)
        token = jwt.encode({'id': response.user_id)}, SECRET_KEY, algorithm='HS256')
        return Response(token.decode('utf-8'), status=status.HTTP_204_NO_CONTENT)



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
    if request.method == 'POST':
        try:
            serializer = InstanceSerializer(user_id=request.user.id, instance=request.POST.get('instance', ''),
                                            instance_provider=request.POST.get('instance_provider',''),
                                            provider_service=request.POST.get('provider_service', ''))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        except:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            instances = Instance.objects.filter(user_id=request.user.id)
            serializer = InstanceSerializer(instances, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Instance.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)




'''
# POST new INSTANCE
@api_view(['POST'])
'''
'''

@app.route('/report')
def pings():
    session_user_id = str(current_user.get_id())

    # get list of hostnames for session user
    hostnames = Hostname.query.filter_by(user_id=session_user_id).all()

    # get length of session user hostnames
    hostname_length = len(hostnames)

    # ping results to populate table. Display only unique hostnames
    ping_results_table = PingResults.query.filter_by(user_id=session_user_id).order_by("update_time desc").limit(hostname_length).all()

    # ping results for charts. Display ALL hostnames for time series view
    ping_results_chart = PingResults.query.filter_by(user_id=session_user_id).order_by("update_time asc").all()

    # parse datetime in ping results and turn into the following format: "mm/dd/yyyy hh:mm"


    # format ping results into google chart javasript format.


    return render_template('pings.html', hostnames_table = ping_results_table)


@app.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        username_form = request.form['username']
        password_form = request.form['password']
        verify_password_form = request.form['verify_password']
        email_form = request.form['email']

        if password_form == verify_password_form:
            password_match = True
        else:
            password_match = False
            error = "Passwords do not match"
            return render_template('signup.html', error=error)

        username_query = Identifer.query.filter_by(username=username_form).all()

        if username_query:
            unique_username = False
            error = "That username already exists"
            return render_template('signup.html', error=error)
        else:
            unique_username = True

        if password_match == True and unique_username == True:
            pw_hash = bcrypt.generate_password_hash(password_form)

            new_user = Identifer(username_form, pw_hash, email_form)

            db.session.add(new_user)
            db.session.commit()

            user_id = find_user_id(username_form,password_form)
            user = User(user_id,username_form, password_form)
            login_user(user, force=True)
            return render_template('hostnames.html')
        else:
            return render_template('signup.html', username_value = username_form)
    else:
        return render_template('signup.html')
'''
