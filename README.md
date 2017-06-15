# semaphore-django

![semaphore_banner](https://cloud.githubusercontent.com/assets/3104259/20028905/dd2e7cd8-a2fa-11e6-88a3-b59ec2889714.jpeg)

## Architecture

Semaphore consists of two parts:
* "the UI": sign in, sign up, add hostnames to your account, and view your ping results.

* "ping service": set on an interval, this service will access the hostname database and concurrently ping them. The results are stored in another database that the UI can access to display the results.  

## User interface

![semaphore_screen](https://cloud.githubusercontent.com/assets/3104259/25326612/d17dd616-2885-11e7-8290-01fb5d4c74e0.png)


## Set Up

* Semaphore is built on `Python 3.5.2`
* Web Server Framework: `Django`
* Database: `postgreSQL` hosted on `AWS RDS`
* The ping service currently runs as a multi-threaded script set on a 60 second interval. I recommend hosting this project on your cloud container of your choice, and execute the script, so that it can run continuously.

*Running Semaphore locally*

* Run `python app.py` and navigate to `http://localhost:5000` to access the main app UI.
* Run `python ping_service.py` in a separate terminal window to fire up the service that pings the hostnames you add to monitor.

## Understanding the Semaphore logic

There are a lot of moving parts in Semaphore's logic.

The first piece of importance is the UI `app.py`. The Semaphore interface allows users to add hostnames into the database (as well as delete hostnames), manage hostnames, and view reports
on their hostname's ping latency.

The second piece is the script that both checks the database for new hostnames, and executes the hostname ping `ping_service.py`. At the beginning of every minute, the ping service first queries the `hostname` table to update its list of hostnames. It then uses Python's multi-thread to execute 4 hostname pings at a time. Results from the pings are stored in the `pingsresult` table.


## Working with the database

Semaphore uses PostgreSQL hosted on AWS RDS, however Django's backend settings do not discriminate between a cloud or locally based database, so simply add your credentials to `django.backends` in `settings.py`

  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': '',
          'USER': '',
          'PASSWORD': '',
          'HOST': '',
          'PORT': '',
      }
  }


2. Instance
  * `user_id`
  * `instance` - hostname for cloud instance
  * `instance_provider` - Amazon Web Services, Google Cloud Platform, Microsoft Azure
  * `provider_service` - Specific service used on Cloud Platform (ex. EC2, or GCP App Engine)

3. Ping Results
  * `user_id`
  * `instance`
  * `min_ping`- minimum ping latency
  * `max_ping` - maximum ping latency
  * `avg_ping` - average ping latency
  * `update_time` - time that ping was executed

## App Pages

* `localhost:5000/`: default main page
* `/signup`: user sign up page
* `/signin`: user sign in page
* `/manage`: manage your hostnames
* `/report`: view the ping status of all the hostnames you are monitoring
