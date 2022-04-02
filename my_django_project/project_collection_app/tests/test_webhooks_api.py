from django.urls import reverse, resolve
from django.test import SimpleTestCase
from project_collection_app.views import WebhookList
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User

class ApiUrlsTests(SimpleTestCase):

    def test_get_github_projects_is_resolved(self):
        url = reverse('webhooks')
        self.assertEquals(resolve(url).func.view_class, WebhookList)

class GithubProjectsAPIViewTests(APITestCase):

    webhooks_url = reverse('webhooks')

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testuser123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        pass

    def test_get_webhooks_authenticated(self):
        response = self.client.get(self.webhooks_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_webhooks_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.webhooks_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_webhook_authenticated(self):
        data = {
            "url": "http://localhost.foobar_receiver"
        }
        response = self.client.post(self.webhooks_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['url'], 'http://localhost.foobar_receiver')

    def test_post_webhook_unauthenticated(self):
        data = {
            "url": "http://localhost.foobar_receiver"
        }
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(self.webhooks_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)


class WebhookDetailAPIViewTests(APITestCase):
    webhooks_url = reverse('webhooks')
    webhook_url_user1 = reverse('webhook_entry', args=[1])
    webhook_url_user2 = reverse('webhook_entry', args=[2])

    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='user111')
        self.token1 = Token.objects.create(user=self.user1)
        self.client1 = APIClient()
        self.client1.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)

        self.user2 = User.objects.create_user(username='user2', password='user222')
        self.token2 = Token.objects.create(user=self.user2)
        self.client2 = APIClient()
        self.client2.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)

        data1 = {
            "url": "http://localhost.webhook1"
        }

        data2 = {
            "url": "http://localhost.webhook2"
        }

        # This will be used on later tests
        self.data_mod = {
            "url": "http://localhost.webhook1.modified"
        }        

        response1 = self.client1.post(self.webhooks_url, data1, format='json')
        response2 = self.client2.post(self.webhooks_url, data2, format='json')

    def test_get_webhook_authenticated(self):
        response = self.client1.get(self.webhook_url_user1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['url'], 'http://localhost.webhook1')

    def test_get_webhook_unauthenticated(self):
        self.client1.force_authenticate(user=None, token=None)
        response = self.client1.get(self.webhook_url_user1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_webhook_created_by_other_authenticated(self):
        response = self.client1.get(self.webhook_url_user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['url'], 'http://localhost.webhook2')

    def test_modify_webhook_created_by_self_authenticated(self):
        response = self.client1.put(self.webhook_url_user1, self.data_mod, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['url'], 'http://localhost.webhook1.modified')

    def test_modify_webhook_created_by_other_authenticated(self):
        response = self.client1.put(self.webhook_url_user2, self.data_mod, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_webhook_created_by_self_authenticated(self):
        response = self.client1.delete(self.webhook_url_user1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_webhook_created_by_other_authenticated(self):    
        response = self.client1.delete(self.webhook_url_user2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)