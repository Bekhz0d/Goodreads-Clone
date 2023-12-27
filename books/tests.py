from django.test import TestCase
from django.urls import reverse
from books.models import CustomUser, BookAuthor, Book, Author


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"),)

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book 1", description="Description 1", isbn="9876795685666")
        book2 = Book.objects.create(title="Book 2", description="Description 2", isbn="2354635675656")
        book3 = Book.objects.create(title="Book 3", description="Description 3", isbn="1278854378587")

        response = self.client.get(reverse("books:list") + "?page_size=2")

        for book in [book1, book2]:
            self.assertContains(response, book.title)
        self.assertNotContains(response, book3.title)
        
        response = self.client.get(reverse('books:list') + '?page=2')

        self.assertContains(response, book3.title)

    def test_detail_page(self):
        book = Book.objects.create(title="Book 1", description="Description 1", isbn="9876795685666")
            
        response = self.client.get(reverse("books:detail_page", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)
        self.assertContains(response, book.isbn)

    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description="Description 1", isbn="9876795685666")
        book2 = Book.objects.create(title="Guide", description="Description 2", isbn="2354635675656")
        book3 = Book.objects.create(title="Atomic", description="Description 3", isbn="1278854378587")       
        
        response = self.client.get(reverse('books:list') + "?q=sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse('books:list') + "?q=guide")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)
        
        response = self.client.get(reverse('books:list') + "?q=atomic")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book2.title)

    def test_book_author(self):
        book = Book.objects.create(title="Book 1", description="Description 1", isbn="9876795685666")
        author1 = Author.objects.create(first_name="John", last_name="Doe", email="dohn@gmail.com", bio="Good person")
        author2 = Author.objects.create(first_name="Bekhzod", last_name="Nabijonov", email="Bek@gmail.com", bio="Good person")
        author3 = Author.objects.create(first_name="Bekhzod3", last_name="Nabijonov3", email="Bek3@gmail.com", bio="Good person...")

        BookAuthor.objects.create(book=book, author=author1)
        BookAuthor.objects.create(book=book, author=author2)

        response = self.client.get(reverse('books:detail_page', kwargs={'id': book.id}))
        for book_author in book.bookauthor_set.all():
            self.assertContains(response, book_author.author.full_name())
        self.assertNotContains(response, author3.full_name)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Book 1", description="Description 1", isbn="9876795685666")
        user = CustomUser.objects.create(
            username="Bekhzod",
            first_name="Bekhzod",
            last_name="Nabijonov",
            email="Bekhzod@gmail.com",
            )
        user.set_password("examplepassword")
        user.save()

        self.client.login(username="Bekhzod", password="examplepassword")

        self.client.post(reverse('books:reviews', kwargs={'id': book.id}), data={
            "stars_given": 3,
            "comment": "Nice book"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].stars_given, 3)
        self.assertEqual(book_reviews[0].comment, "Nice book")
        self.assertEqual(book_reviews[0].book, book)
        self.assertEqual(book_reviews[0].user, user)
        
    def test_review_stars_given(self):
        book = Book.objects.create(title="Book 1", description="Description 1", isbn="9876795685666")
        user = CustomUser.objects.create(
            username="Bekhzod",
            first_name="Bekhzod",
            last_name="Nabijonov",
            email="Bekhzod@gmail.com",
            )
        user.set_password("examplepassword")
        user.save()

        self.client.login(username="Bekhzod", password="examplepassword")

        self.client.post(reverse('books:reviews', kwargs={'id': book.id}), data={
            "stars_given": 6,
            "comment": "Nice book"
        })

        book_reviews = book.bookreview_set.all()
        
        self.assertEqual(book_reviews.count(), 0)

