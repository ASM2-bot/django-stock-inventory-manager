from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse
import csv
from django.contrib import messages
from .forms import StockCreateForm, StockSearchForm, StockUpdateForm
from .forms import IssueForm, ReceiveForm
from .forms import ReorderLevelForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Stock
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy


def home(request):
    title = 'Welcome: This is the Home Page'
    context = {
        "title": title,
    } 
    return render(request, "home.html", context)


@login_required(login_url='login')
@never_cache
def list_items(request):
    title = 'LIST OF ITEMS'
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all()

    if request.method == 'POST' and form.is_valid():
        category = form.cleaned_data.get('category')
        item_name = form.cleaned_data.get('item_name')
        export_to_CSV = form.cleaned_data.get('export_to_CSV')

        queryset = Stock.objects.filter(
            category__name__icontains=category,
            item_name__icontains=item_name
        )

        if export_to_CSV:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List_of_stock.csv"'

            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])

            for stock in queryset:
                writer.writerow([stock.category.name, stock.item_name, stock.quantity])

            return response  

    context = {
        "title": title,
        "form": form,
        "queryset": queryset,
    }    
    return render(request, "list_items.html", context)


@login_required(login_url='login')
@never_cache
def add_items(request):
    form = StockCreateForm(request.POST or None)

    if form.is_valid():
        form.save()
        messages.success(request, 'Item successfully added.')
        return redirect('list_items')  # Utilisez le nom de l'URL plutôt que le chemin

    context = {
        "form": form,
        "title": "Add Item",
    }
    return render(request, "add_items.html", context)


@login_required(login_url='login')
@never_cache
def update_items(request, pk):
    stock = get_object_or_404(Stock, id=pk)

    if request.method == 'POST':
        form = StockUpdateForm(request.POST)
        if form.is_valid():
            # Get the Category object from the name
            category_name = form.cleaned_data['category']
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                form.add_error('category', 'Category does not exist.')
                return render(request, 'add_items.html', {'form': form})

            stock.category = category
            stock.item_name = form.cleaned_data['item_name']
            stock.quantity = form.cleaned_data['quantity']
            stock.save()
            messages.success(request, 'Item successfully updated.')
            return redirect('list_items')
    else:
        form = StockUpdateForm(initial={
            'category': stock.category.name,
            'item_name': stock.item_name,
            'quantity': stock.quantity
        })

    context = {
        'form': form,
        'title': f'Update {stock.item_name}'
    }
    return render(request, 'add_items.html', context)


@login_required(login_url='login')
@never_cache
def delete_items(request, pk):
    stock = get_object_or_404(Stock, id=pk) 

    if request.method == 'POST':
        stock.delete()
        messages.success(request, 'Item successfully deleted.')
        return redirect('list_items')

    return render(request, 'delete_items.html', {'stock': stock})


@login_required(login_url='login')
@never_cache
def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    return render(request, 'stock_detail.html', {'stock': stock})

from django.contrib import messages


@login_required(login_url='login')
@never_cache
def issue_items(request, pk):
    queryset =Stock.objects.get(id=pk)
    form =IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.receive_quantity=0
        instance.quantity -= instance.issue_quantity
        messages.success(request, "Issued Successfuly." + str(instance.quantity)+ str(instance.item_name) +  "s now left in Store" )
        instance.save()

        return redirect('/stock_detail/' +str(instance.id))
    

    context = { 
        "title":'Issue'+str(queryset.item_name),
        "queryset":queryset,
        "form":form,
        "username":'Issue By:'+ str(request.user),
    }
    return render(request, "main/issue_items.html",context)

@login_required(login_url='login')
@never_cache
def receive_items(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity=0
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, f"Received SUCCESSFULLY. {instance.quantity} {instance.item_name}s now in Store")
        return redirect('stock_detail', pk=instance.id)

    context = {
        "title": f'Receive {queryset.item_name}',
        "instance": queryset,
        "form": form,
        "username": f'Receive By: {request.user}',
    }
    return render(request, "main/receive_items.html", context)


@login_required(login_url='login')
@never_cache
def reorder_level(request, pk):
    queryset = get_object_or_404(Stock, id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, f"Reorder level for {instance.item_name} is updated to {instance.reorder_level}")
        return redirect("list_items")

    context = {
        "instance": queryset,
        "form": form,
    }
    return render(request, "add_items.html", context)


@login_required(login_url='login')
@never_cache
def update_reorder_level(request, id):
    item = get_object_or_404(Stock, id=id)
    
    if request.method == 'POST':
        form = ReorderLevelForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Reorder level updated successfully.")
            return redirect('list_items')
    else:
        form = ReorderLevelForm(instance=item)

    return render(request, 'update_reorder_level.html', {'form': form, 'item': item})


@login_required(login_url='login')
@never_cache
def dashboard(request):
    # Ajoutons quelques statistiques pour le dashboard
    total_items = Stock.objects.count()
    low_stock_items = Stock.objects.filter(quantity__lte=10).count()  # Ajustez selon vos besoins
    
    context = {
        'total_items': total_items,
        'low_stock_items': low_stock_items,
    }
    return render(request, 'home.html', context)    

 
# ===== VUES D'AUTHENTIFICATION CORRIGÉES =====

@method_decorator(never_cache, name='dispatch')
class CustomLoginView(LoginView):
    template_name = 'login.html' 
    
    def get_success_url(self):
        # Redirige vers le home après connexion réussie
        return reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, f'Bienvenue {form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = 'home'  # Redirige vers la page d'accueil après déconnexion
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'Vous êtes maintenant déconnecté.')
        return super().dispatch(request, *args, **kwargs)
    



