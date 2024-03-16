import pika
import json
from faker import Faker
from mongoengine import connect
from mongoengine import Document, StringField, BooleanField

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent_message = BooleanField(default=False)

connect('contacts', host='mongodb+srv://divan4ik223:03b.kz2005@dzweb8.m87srrp.mongodb.net/?retryWrites=true&w=majority&appName=dzweb8')


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='contact_ids')


fake = Faker()

for _ in range(10):
    fullname = fake.name()
    email = fake.email()

    contact = Contact(fullname=fullname, email=email)
    contact.save()

    channel.basic_publish(
        exchange='',
        routing_key='contact_ids',
        body=json.dumps({'contact_id': str(contact.id)})
    )

    print(f"Contact {fullname} with email {email} added to database and queued for email sending")

connection.close()
