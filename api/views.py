# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum, F
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import SalesItem, Book


class GetAuthors(APIView):
    def get(self, request):
        status = 200
        if 'author' in request.GET:
            books = Book.objects.filter(author__name=request.GET['author']).values('isbn')
            if books:
                response = {'books': books}
            else:
                response = {'author': 'Author Not found'}
                status = 404
        else:
            authors = SalesItem.objects.values('book__author__name').annotate(total_price=F('item_price') * F('quantity')).order_by('-total_price').values('book__author__name', 'total_price')[:10]
            response = {'authors': authors}

        return Response(response, status=status)

def answers(request):
    return render(request, 'api/Answer.html')


'''

Q1: Who are the first 10 authors ordered by date_of_birth?

SELECT name as Author Name FROM authors ORDER_BY date_of_birth;

Q2: What is the sales total for the author named “Lorelai Gilmore”?

SELECT isbn as BookName books FROM  WHERE books.author_id=(SELECT id FROM authors WHERE name="Lorelai Gilmore");

Q3: What are the top 10 performing authors, ranked by sales revenue?

SELECT name AS AuthorName, item_price*quantity AS TotalPrice FROM authors JOIN salesitems ON 
    salesitems.book_id=books.id JOIN books ON books.author_id= authors.id ORDER BY TotalPrice DESC LIMIT 10; 

'''