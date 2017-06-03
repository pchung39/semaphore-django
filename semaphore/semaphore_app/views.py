from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import *
from .signup_form import UserCreateForm
from django.contrib.auth.decorators import login_required


def lander(request):
    return render(request, 'index.html')

# posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')

def signin(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('lander')
        else:
            error = 'We could not find the user'
            return render(request, 'signin.html', {'error': error})
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('lander')
    else:
        form = UserCreateForm()
    return render(request, 'signup.html', {'form': form})

# TODO: make adding a hostname a pop up instead of a page

'''
@login_required
def select_service():
    if request.method == 'POST':
        hostname_form = request.form['hostname']
        hostname_provider_form = request.form['hostname_provider']
        # user_id = str(current_user.get_id())

        new_hostname = Hostname(user_id, hostname_form, hostname_provider_form)

        db.session.add(new_hostname)
        commit = db.session.commit()

        # need to add logic to deal with erroneous posts
        # looks like it returns "None" if no errors

        message = "'%s' was added to the Monitor list" % hostname_form
        return render_template('hostnames.html', message=commit)

    else:
        return render(request, 'hostnames.html', )
'''


@login_required
def manage_services(request):

    instances = Instance.objects.all().filter(user_id=request.user.id).values()
    return render(request, 'manage.html', { 'instances': instances })
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

def logout(request):
    logout(request)
    return render(request, 'index.html')
