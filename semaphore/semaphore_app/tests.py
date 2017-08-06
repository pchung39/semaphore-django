from django.test import TestCase
from django.contrib.auth.models import User
from .serializers import *
from .models import *

class InstanceTest(TestCase):

	def setUp(self):
		user = User.objects.create(username="paul",email="paul@gmail.com")
		user.set_password("banana")
		user.save()
		test_user = User.objects.get(username="paul")
		Instance.objects.create(user=test_user, instance="www.google.com",
								instance_provider="AWS",
								provider_service="EC2")

	def test_instance(self):
		instance = Instance.objects.get(instance="www.google.com")
		serializer = InstanceSerializer(instance)
		self.assertEqual(serializer.data["instance_provider"], "AWS")
		self.assertEqual(serializer.data["provider_service"], "EC2")
