from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Book, Review


class BookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="12345"
        )
        self.book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            author="J.K. Rowling",
            price="14.99",
        )
        self.review = Review.objects.create(
            book=self.book,
            author=self.user,
            review='"This is a great book, and a must read!"',
        )

    def test_book_listing(self):
        self.assertEqual(
            f"{self.book.title}", "Harry Potter and the Philosopher's Stone"
        )
        self.assertEqual(f"{self.book.author}", "J.K. Rowling")
        self.assertEqual(f"{self.book.price}", "14.99")

    def test_book_list_view(self):
        response = self.client.get(reverse("book_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Harry Potter")
        self.assertTemplateUsed(response, "books/book_list.html")

    def test_book_detail_view(self):
        response = self.client.get(self.book.get_absolute_url())
        no_response = self.client.get("/books/12345/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Harry Potter")
        self.assertContains(response, "This is a great book, and a must read!")
        self.assertTemplateUsed(response, "books/book_detail.html")
