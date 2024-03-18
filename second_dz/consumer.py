import pika
import json
import time
from mongoengine import connect
from mongoengine import Document, StringField, BooleanField

class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    sent_message = BooleanField(default=False)


connect('contacts', host='link')


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='contact_ids')

def callback(ch, method, properties, body):
    contact_id = json.loads(body)['contact_id']
    contact = Contact.objects(id=contact_id).first()

    if contact:
        print(f"Sending email to {contact.fullname} at {contact.email}")
        time.sleep(3)

        contact.sent_message = True
        contact.save()
        print(f"Email sent to {contact.fullname}")
    else:
        print(f"Contact with ID {contact_id} not found in database")

# Підписка на чергу
channel.basic_consume(queue='contact_ids', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
