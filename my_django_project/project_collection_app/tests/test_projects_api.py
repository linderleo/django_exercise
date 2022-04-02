from django.urls import reverse, resolve
from django.test import SimpleTestCase
from project_collection_app.views import GithubProjectList
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User

class ApiUrlsTests(SimpleTestCase):

    def test_get_github_projects_is_resolved(self):
        url = reverse('github_projects')
        self.assertEquals(resolve(url).func.view_class, GithubProjectList)

class GithubProjectsAPIViewTests(APITestCase):

    github_projects_url = reverse('github_projects')

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testuser123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def tearDown(self):
        pass

    def test_get_github_projects_authenticated(self):
        response = self.client.get(self.github_projects_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_get_github_projects_unauthenticated(self):
        self.client.force_authenticate(user=None, token=None)
        response = self.client.get(self.github_projects_url)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_project_authenticated(self):
        data = {
            "name": "added project",
            "description": "this is what it is",
            "link": "http://localhost.foobar",
            "rating": 5
        }
        response = self.client.post(self.github_projects_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'added project')

    def test_post_project_unauthenticated(self):
        data = {
            "name": "another added project",
            "description": "this is something",
            "link": "http://localhost.foo",
            "rating": 1
        }
        self.client.force_authenticate(user=None, token=None)
        response = self.client.post(self.github_projects_url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_project_false_data_authenticated(self):
        false_data = {
            "name": "",
            "description": "",
            "link": "",
            "rating": 'X'
        }
        response = self.client.post(self.github_projects_url, false_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        #self.assertEqual(response.data['name'], 'added project')

class ProjectDetailAPIViewTests(APITestCase):
    github_projects_url = reverse('github_projects')
    github_project_url_user1 = reverse('project_entry', args=[1])
    github_project_url_user2 = reverse('project_entry', args=[2])

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
            "name": "created by user 1",
            "description": "this is something",
            "link": "http://localhost.user1",
            "rating": 1
        }

        data2 = {
            "name": "created by user 2",
            "description": "this is something",
            "link": "http://localhost.user2",
            "rating": 2
        }

        # This will be used on later tests
        self.data_mod = {
            "name": "modified by user 1",
            "description": "this is something",
            "link": "http://localhost.user1",
            "rating": 1
        }        

        response1 = self.client1.post(self.github_projects_url, data1, format='json')
        response2 = self.client2.post(self.github_projects_url, data2, format='json')

    def test_get_project_entry_authenticated(self):
        response = self.client1.get(self.github_project_url_user1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'created by user 1')

    def test_get_project_entry_unauthenticated(self):
        self.client1.force_authenticate(user=None, token=None)
        response = self.client1.get(self.github_project_url_user1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_project_entry_created_by_other_authenticated(self):
        response = self.client1.get(self.github_project_url_user2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'created by user 2')

    def test_modify_project_entry_created_by_self_authenticated(self):
        response = self.client1.put(self.github_project_url_user1, self.data_mod, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'modified by user 1')

    def test_modify_project_entry_created_by_other_authenticated(self):
        response = self.client1.put(self.github_project_url_user2, self.data_mod, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_project_entry_created_by_self_authenticated(self):
        response = self.client1.delete(self.github_project_url_user1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_project_entry_created_by_other_authenticated(self):    
        response = self.client1.delete(self.github_project_url_user2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)