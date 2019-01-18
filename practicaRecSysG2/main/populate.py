from django.core import exceptions

from main.models import Rating, Book, User
import csv


path = "datos"


def deleteTables():
    Rating.objects.all().delete()
    Book.objects.all().delete()
    User.objects.all().delete()
    

def populate_books():
    print("Loading books...")
    
    with open(path + "\\books.csv", encoding = "latin-1") as f:
        reader = csv.reader(f, delimiter = ";", quoting = csv.QUOTE_MINIMAL)
        [w_isbn, w_title, w_author, w_yearPub, w_publisher] = next(reader)
        
        # Parametro que indica cuantas tuplas se insertaran en la base de datos
        limit = 0
        while limit <=3201:
            try:
                [w_isbn, w_title, w_author, w_yearPub, w_publisher] = next(reader)
                
                Book.objects.create(ISBN = w_isbn.strip(),
                                    title = w_title.strip(),
                                    author = w_author.strip(),
                                    publicationYear = w_yearPub.strip(),
                                    publisher = w_publisher.strip())
                
                limit = limit + 1
            except:
                print("Error al insertar libro: " + w_isbn.strip())
    
    
            if limit%1000 == 0: 
                print("1000 ratings processed...")
    
    print("Books inserted: " + str(Book.objects.count()))
    print("--------------------------------------------")


def populate_ratings():
    print("Loading ratings...")
    
    with open(path + "\\ratings.csv", encoding = "latin-1") as f:
        reader = csv.reader(f, delimiter = ";", quoting = csv.QUOTE_MINIMAL)
        limit = 0
        [userID, bookID, valueR] = next(reader)
        
        while limit <=7635:
            [userID, bookID, valueR] = next(reader)
            
            try:
                w_user = User.objects.get(id = int(userID.strip()))
            except exceptions.ObjectDoesNotExist as e1:
                w_user = User.objects.create(id = int(userID.strip()))
            
            try:
                w_book = Book.objects.get(ISBN = bookID.strip())
            except exceptions.ObjectDoesNotExist as e2:
                print("Error al recuperar libro: " + bookID.strip())
            
            Rating.objects.create(user = w_user,
                                  book = w_book,
                                  ratingValue = int(valueR.strip()))
                
            limit = limit + 1
            
            if limit%1000 == 0: 
                print("1000 ratings processed...")
        
    print("Rating inserted: " + str(Rating.objects.count()))
    print("--------------------------------------------")
    

def populateDatabase():
    deleteTables()

    populate_books()
    populate_ratings()
    print("Finished database population")

if __name__ == '__main__':
    populateDatabase()