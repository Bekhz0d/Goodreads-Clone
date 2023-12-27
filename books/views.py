from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
# from django.views.generic import DetailView, ListView
from books.forms import BookReviewForm
from books.models import Book, BookReview
from django.core.paginator import Paginator


# class BooksView(ListView):
#     template_name = 'books/list.html'
#     # model = Book
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by = 2


class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')

        search_query = request.GET.get('q', '')
        if search_query:
            books = books.filter(title__icontains=search_query)

        page_size = request.GET.get('page_size', 2)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_num)

        return render(request, "books/list.html", {"page_obj": page_obj, "search_query": search_query})


# class BookDetailView(DetailView):
#     model = Book
#     template_name = 'books/detail.html'
#     # pk_url_kwarg = 'id'


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm()

        return render(request, "books/detail.html", {"book": book, "review_form": review_form})    
        

class AddReviewView(View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForm(data=request.POST)

        if review_form.is_valid():
            BookReview.objects.create(
                book=book,
                user=request.user,
                stars_given=review_form.cleaned_data['stars_given'],
                comment=review_form.cleaned_data['comment']
            )

            return redirect(reverse('books:detail_page', kwargs={'id': book.id}))
        return render(request, 'books/detail.html', {'book': book, 'review_form': review_form})
