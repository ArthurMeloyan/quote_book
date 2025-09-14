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


def like(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    quote.likes += 1
    quote.save(update_fields=['likes'])

    return redirect('random_quote')

def dislike(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)
    quote.dislikes += 1
    quote.save(update_fields=['dislikes'])

    return redirect('random_quote')


def add_quote_view(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('random_quote')
    else:
        form = QuoteForm()


    context = {
        'form': form,
    }

    return render(request, 'quotes/create.html', context)