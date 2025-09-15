from django.shortcuts import render, get_object_or_404, redirect
from .models import Quote
import random
from .forms import QuoteForm
# Create your views here.

page_views = 0  # views counter

def random_quote_view(request):
    global page_views
    page_views += 1

    # Get all quotes
    quotes = Quote.objects.all()

    # Check if there are no quotes at all
    if not quotes:
        context = {'page_views': page_views}
        return render(request, 'quotes/index.html', context)
    
    # using weight for random quote view
    total_weight = sum(q.weight for q in quotes)
    random_num = random.uniform(0, total_weight)

    cumulative_weight = 0
    selected_quote = None

    for quote in quotes:
        cumulative_weight += quote.weight
        if random_num <= cumulative_weight:
            selected_quote = quote
            break  # Found a "winner" so can breake 
    
    # Update views counter for quote
    if selected_quote:
        selected_quote.views += 1
        selected_quote.save(update_fields=['views']) 

    context = {
        'quote': selected_quote,
        'page_views': page_views,
    }

    return render(request, 'quotes/index.html', context)

# Funtion for like logic 
def like(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)  # get all quotes from db
    quote.likes += 1  # Increment like
    quote.save(update_fields=['likes'])  # Save new likes count

    next_page = request.GET.get('next', '/')  # Check if we on main page or on Top-10 page

    return redirect(next_page)  # redirect to main page if we're on the main page, either stay on top-10

# Function for dislike logic, same as for like 
def dislike(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    quote.dislikes += 1
    quote.save(update_fields=['dislikes'])

    next_page = request.GET.get('next', '/')

    return redirect(next_page)

# Function for adding quote
def add_quote_view(request):
    if request.method == 'POST':  # Check if request method is POST
        form = QuoteForm(request.POST)
        if form.is_valid():  # Check for valid request form
            form.save()
            return redirect('random_quote')  # After quote add redirect to main page
    else:
        form = QuoteForm()


    context = {
        'form': form,
    }

    return render(request, 'quotes/create.html', context)


# Function to view list of top 10 quotes
def top_quotes_view(request):

    sort_by = request.GET.get('sort', 'likes') # Get parameter for sort, if there is no so by default it's 'likes'
    allowed_sort_params = {  # Allowed params for sorting
        'likes': '-likes',
        'dislikes': '-dislikes',
        'views': '-views',
        'newest': '-created_at'
    }

    translated = {
        'likes': 'лайкам',
        'dislikes': 'дизлайкам',
        'views': 'просмотрам',
        'newest': 'дате добавления'
    }
    order_param = allowed_sort_params.get(sort_by, '-likes')  # Choose parameter from allowed sorted, if there is no so by default it's '-likes'
    quotes = Quote.objects.all().order_by(order_param)[:10]  # Get all quotes and choose first 10 by order parameter
    context = {
        'quotes': quotes,
        'current_sort': sort_by,
        'title': f'Топ-10 цитат по {translated[sort_by]}'
    }
    return render(request, 'quotes/top_10.html',context)