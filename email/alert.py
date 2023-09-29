import django
from django.core.mail import send_mail
from django.template.loader import render_to_string
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()

def clinical_msg (data): # dict
    msg_plain = render_to_string('templates/clinical_notif.txt', data)
    msg_html = render_to_string('templates/clinical_notif.html', data)

    send_mail(
        'Test Email',
        msg_plain,
        'from-email <notif@nih.gov>',
        ['RECIPIENT'],
        html_message=msg_html
    )

def pubmed_msg (data): # dict
    msg_plain = render_to_string('templates/pubmed_notif.txt', data)
    msg_html = render_to_string('templates/pubmed_notif.html', data)

    send_mail(
        'Test Email',
        msg_plain,
        'from-email <notif@nih.gov>',
        ['RECIPIENT'],
        html_message=msg_html
    )

def grant_msg (data): # dict
    msg_plain = render_to_string('templates/grant_notif.txt', data)
    msg_html = render_to_string('templates/grant_notif.html', data)

    send_mail(
        'Test Email',
        msg_plain,
        'from-email <notif@nih.gov>',
        ['RECIPIENT'],
        html_message=msg_html
    )
    
def test_msg (sub, msg, recip):
    send_mail(
        f'{sub}',
        f'{msg}',
        'ncatsrdas@mail.nih.gov',
        [f'{recip}']
    )