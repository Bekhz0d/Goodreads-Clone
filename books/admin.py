from django.contrib import admin
from .models import Book, Author, BookAuthor, BookReview


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title',  'isbn', 'description',)
    search_fields = ('title', 'isbn', 'description',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',)
    search_fields = ('first_name', 'last_name', 'email',)


@admin.register(BookAuthor)
class BookAuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    pass
