import shelve
from django.shortcuts import render, get_object_or_404
from main.populate import populateDatabase
from main.recommendations import  transformPrefs, calculateSimilarItems, getRecommendedItems, topMatches
from main.models import Rating, Book, User
from main.forms import UserForm, BookForm

from django.db.models import Avg


# Funcion que carga en el diccionario Prefs todas las puntuaciones de usuarios a peliculas. Tambien carga el diccionario inverso y la matriz de similitud entre items
# Serializa los resultados en dataRS.dat

def loadDict():
    Prefs={}   # matriz de usuarios y puntuaciones a cada a items
    shelf = shelve.open("dataRS.dat")
    ratings = Rating.objects.all()
    for ra in ratings:
        user = int(ra.user.id)
        itemid = ra.book.ISBN
        rating = float(ra.ratingValue)
        Prefs.setdefault(user, {})
        Prefs[user][itemid] = rating
    shelf['Prefs']=Prefs
    shelf['ItemsPrefs']=transformPrefs(Prefs)
    shelf['SimItems']=calculateSimilarItems(Prefs, n=10)
    shelf.close()

#  CONJUNTO DE VISTAS

def index(request): 
    return render(request,'index.html')


def populateDB(request):
    populateDatabase() 
    return render(request,'populate.html')


def loadRS(request):
    loadDict()
    return render(request,'loadRS.html')


#APARTADO A
def search(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(User, pk=idUser)
            return render(request,'ratedBooks.html', {'usuario':user})
    form=UserForm()
    return render(request,'search_user.html', {'form':form })

# Apartado B
def topThree(request):
    if request.method == 'GET':
        book = Book.objects.all()
        books = book.annotate(average_rating=Avg('rating__ratingValue')).order_by('average_rating')[:3]
        return render(request, 'topThreeBooks.html', {'books':books})
    

# APARTADO C
def similarBooks(request):
    book = None
    if request.method=='GET':
        form = BookForm(request.GET, request.FILES)
        if form.is_valid():
            idBook = form.cleaned_data['isbn']
            book = get_object_or_404(Book, pk=idBook)
            shelf = shelve.open("dataRS.dat")
            ItemsPrefs = shelf['ItemsPrefs']
            shelf.close()
            recommended = topMatches(ItemsPrefs, idBook, n=2)
            items=[]
            for re in recommended:
                item = Book.objects.get(ISBN=re[1])
                items.append(item)
            return render(request,'similarBooks.html', {'book': book,'books': items})
    form = BookForm()
    return render(request,'search_book.html', {'form': form})


# APARTADO D
def recommendedBooks(request):
    if request.method=='GET':
        form = UserForm(request.GET, request.FILES)
        if form.is_valid():
            idUser = form.cleaned_data['id']
            user = get_object_or_404(User, pk=idUser)
            shelf = shelve.open("dataRS.dat")
            Prefs = shelf['Prefs']
            SimItems = shelf['SimItems']
            shelf.close()
            rankings = getRecommendedItems(Prefs, SimItems, int(idUser))
            recommended = rankings[:2]
            items = []
            for re in recommended:
                item = Book.objects.get(pk=re[1])
                items.append(item)
            return render(request,'recommendationItems.html', {'user': user, 'items': items})
    form = UserForm()
    return render(request,'search_user.html', {'form': form})
