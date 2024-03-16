import json
from mongoengine import connect
from mongoengine import Document, StringField, ListField, ReferenceField

class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()


# Підключення до бази даних MongoDB
connect(db='first_bd', host='mongodb+srv://divan4ik223:03b.kz2005@dzweb8.m87srrp.mongodb.net/?retryWrites=true&w=majority&appName=dzweb8')

# Завантаження даних з JSON-файлів та їх збереження в базі даних
def load_authors_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            author_name = author_data['fullname']
            author = Author.objects(fullname=author_name).first()
            if not author:
                author = Author(**author_data)
                author.save()

def load_quotes_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author_name = quote_data['author']
            author = Author.objects(fullname=author_name).first()
            if author:
                existing_quote = Quote.objects(quote=quote_data['quote'], author=author).first()
                if not existing_quote:
                    quote_data['author'] = author
                    quote = Quote(**quote_data)
                    quote.save()
            else:
                author = Author(fullname=author_name)
                author.save()
                quote_data['author'] = author
                quote = Quote(**quote_data)
                quote.save()


# Виклик функцій для завантаження даних з файлів
load_authors_from_json('authors.json')
load_quotes_from_json('quotes.json')

def search_quotes(command):
    if command.startswith('name:'):
        author_name = command[len('name:'):].strip()
        author = Author.objects(fullname=author_name).first()
        if author:
            quotes = Quote.objects(author=author)
            return [quote.quote for quote in quotes]
        else:
            return ["Автор '{}' не найден.".format(author_name)]
    elif command.startswith('tag:'):
        tag = command[len('tag:'):].strip()
        quotes = Quote.objects(tags=tag)
        return [quote.quote for quote in quotes]
    elif command.startswith('tags:'):
        tags = command[len('tags:'):].strip().split(',')
        quotes = Quote.objects(tags__in=tags)
        return [quote.quote for quote in quotes]
    elif command == 'exit':
        return None
    else:
        return ["Неверный формат команды."]

while True:
    user_input = input().strip()
    results = search_quotes(user_input)
    if results is None:
        break
    else:
        for result in results:
            print(result)
