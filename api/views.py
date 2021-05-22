# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Sum, F
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import SalesItem, Book, Author


class GetAuthors(APIView):
    def get(self, request):
        status = 200
        if 'author' in request.GET:
            authors = SalesItem.objects.filter(book__author__name=request.GET['author']).values(
                'book__author__name').annotate(total_price=F('item_price') * F('quantity')).annotate(
                total_price=Sum('total_price')).values('book__author__name', 'total_price')
            if authors:
                response = {'authors': authors}
            else:
                response = {'author': 'Author Not found'}
                status = 404
        else:
            authors = SalesItem.objects.values('book__author__name').annotate(
                total_price=F('item_price') * F('quantity')).annotate(total_price=Sum('total_price')).order_by(
                '-total_price').values('book__author__name', 'total_price')[:10]
            response = {'authors': authors}

        return Response(response, status=status)


def answers(request):
    q1 = Author.objects.all().order_by('date_of_birth')[:10]
    q2 = SalesItem.objects.filter(book__author__name='Lorelai Gilmore').values(
                'book__author__name').annotate(total_price=F('item_price') * F('quantity')).annotate(
                total_price=Sum('total_price')).values('book__author__name', 'total_price')
    print(q2)
    q3 = SalesItem.objects.values('book__author__name').annotate(
                total_price=F('item_price') * F('quantity')).annotate(total_price=Sum('total_price')).order_by(
                '-total_price').values('book__author__name', 'total_price')[:10]

    return render(request, 'api/Answer.html', {'q1': q1, 'q2':q2, 'q3':q3})


'''

Q1: Who are the first 10 authors ordered by date_of_birth?

SELECT name, date_of_birth FROM authors ORDER BY date_of_birth ASC LIMIT 10;

Q2: What is the sales total for the author named “Lorelai Gilmore”?

SELECT authors.name, SUM((item_price*quantity)) AS total_price FROM salesitem INNER JOIN book ON 
    (salesitem.book_id=book.id) INNER JOIN authors ON (book.author_id=authors.id) WHERE authors.name='Lorelai Gilmore' GROUP BY authors.name;

Q3: What are the top 10 performing authors, ranked by sales revenue?

SELECT authors.name AS AuthorName, item_price*quantity AS TotalPrice FROM authors JOIN salesitems ON 
    salesitems.book_id=books.id JOIN books ON books.author_id= authors.id ORDER BY TotalPrice DESC LIMIT 10; 

'''
