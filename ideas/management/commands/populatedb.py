from faker import Faker
import requests
import random

from django.core.management.base import BaseCommand

fake = Faker()

class Command(BaseCommand):
    help = 'Populate database with fake data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of posts to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
    
        for i in range(total):
            payload = {"email": f"user{i+1}@mail.com", "password": "testpass"}

            requests.post('http://localhost:8000/auth/register/', data=payload)

            response = requests.post('http://localhost:8000/auth/token/', data=payload)

            token = response.json()['access']
            
            headers = {'Authorization': 'Bearer ' + token}

            for j in range(random.randint(2, 20)):
                payload = {"title": fake.sentence(), "content": fake.text()}
                requests.post('http://localhost:8000/ideas/posts/', data=payload, headers=headers)

            self.stdout.write(self.style.SUCCESS(f'{i+1} users created and 2-20 posts each'))