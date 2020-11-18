from django.shortcuts import render, redirect
from django.contrib import messages
from airtable import Airtable
from dotenv import load_dotenv
import os

load_dotenv()


AT = Airtable(os.getenv('AIRTABLE_MOVIESTABLE_BASE_ID'), 'MOVIES', api_key=os.getenv('AIRTABLE_API_KEY'))

# Create your views here.
def home_page(request):
    user_query = str(request.GET.get('query', ''))
    search_result = AT.get_all(formula="FIND('" + user_query.lower() + "', LOWER({Name}))")
    stuff_for_frontend = {'search_result': search_result}
    return render(request,'movies/movies_stuff.html', stuff_for_frontend)

def create(request):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.insert(data)
            messages.success(request, 'New Movie Added : {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.error(request, 'Error while Creating Movie : {}'.format(e))
    return redirect('/')

def edit(request, movie_id):
    if request.method == 'POST':
        data = {
            'Name': request.POST.get('name'),
            'Pictures': [{'url': request.POST.get('url') or 'https://thumbs.dreamstime.com/b/no-image-available-icon-flat-vector-no-image-available-icon-flat-vector-illustration-132482953.jpg'}],
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notes')
        }
        try:
            response = AT.update(movie_id,data)
            messages.success(request, 'Movie Updated : {}'.format(response['fields'].get('Name')))
        except Exception as e:
            messages.error(request, 'Error while Updating Movie : {}'.format(e))
    return redirect('/')

def delete(request, movie_id):
    try:
        movie_name = AT.get(movie_id)['fields'].get('Name')
        AT.delete(movie_id)
        messages.warning(request, 'Movie Deleted : {}'.format(movie_name))
    except Exception as e:
        messages.error(request, 'Error while Deleting Movie : {}'.format(e))

    return redirect('/')

