from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from rest_framework import status

class TestIdeas(APITestCase):

    def setUp(self):
        # register a user
        self.client = APIClient()

        payload = {"email": "testuser1@mail.com", "password": "testpass"}
        self.client.post(reverse('register'), payload)

        # login the user and get the token
        response = self.client.post(reverse('token_obtain_pair'), payload)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        print("setup is done")
    
    def test_ideas(self):
        # create new post
        payload = {"title": "test title", "content": "test content"}
        response = self.client.post(reverse('posts'), payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['content'], payload['content'])

        # get all posts
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        # get id of a post then get that post
        pk = response.data[0]['id']
        response = self.client.get(reverse('post', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['content'], payload['content'])

        # update the post
        payload = {"title": "test title changed", "content": "test content changed"}
        response = self.client.put(reverse('post', kwargs={'pk': pk}), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['content'], payload['content'])

        # delete the post
        response = self.client.delete(reverse('post', kwargs={'pk': pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # get all posts
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        print("test_ideas is done")
    
    # register a new user, login, set the token bearer and create 15 posts
    def test_ideas_15_posts(self):
        # register a user
        payload = {"email": "testuser2@mail.com", "password": "testpass"}
        self.client.post(reverse('register'), payload)

        # login the user and get the token
        response = self.client.post(reverse('token_obtain_pair'), payload)
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        # create 15 posts
        for i in range(15):
            payload = {"title": "test title " + str(i), "content": "test content " + str(i)}
            self.client.post(reverse('posts'), payload)

        # get all posts
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 15)

        print("test_ideas_15_posts is done")






