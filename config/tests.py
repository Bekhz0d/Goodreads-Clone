from django.urls import reverse
from books.models import Book, BookReview
from users.models import CustomUser
from django.test import TestCase


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Book 1', description='Description 1', isbn='6873673687367')
        user = CustomUser.objects.create(
            username='bekhzod', 
            first_name='Bekhzod',
            last_name='Nabijonov',
            email='bekhzod@gmail.com'
        )
        user.set_password('somepassword')
        user.save()
        review1 = BookReview.objects.create(book=book, user=user, stars_given=2, comment='Yaxshi emas')
        review2 = BookReview.objects.create(book=book, user=user, stars_given=4, comment="Yomon kitob bolmaydi")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=5, comment='Nice book')

        response = self.client.get(reverse('home_page') + '?page_size=2')

        self.assertContains(response, review3.comment)
        self.assertContains(response, review2.comment)
        self.assertNotContains(response, review1.comment)
