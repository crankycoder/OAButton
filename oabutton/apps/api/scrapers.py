from django.core.mail import send_mail
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from oabutton.apps.api.grab_page import load_page
from oabutton.apps.api.models import PendingOpen
import email
import hashlib
import imaplib
import json
import random
import requests


def download_inbox():
    """
    Check inbound mail
    """
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('oabutton@crankycoder.com', 'hackoabutton')
    mail.select("inbox")

    result, data = mail.uid('search', None, "ALL")
    for msg_uid in data[0].split():

        result, data = mail.uid('fetch', msg_uid, '(RFC822)')
        raw_email = data[0][1]

        mail_dict = _process_raw_email(raw_email)

        PendingOpen.objects.create(sender_email="%s <%s>" % mail_dict['from'],
                                   subject=mail_dict['subject'],
                                   email_text=mail_dict['text'],
                                   email_headers=json.dumps(mail_dict['headers']))

        # Label the message as processed (only works with gmail)
        mail.uid('STORE', msg_uid, '+X-GM-LABELS', 'processed')

        # Mark the message as deleted (which is basically archived)
        # TODO: uncomment this
        #mail.uid('STORE', msg_uid, '+FLAGS', '(\Deleted)')


def _process_raw_email(raw_email):
    """
    Return a dictionary with the following keys:
    """
    email_message = email.message_from_string(raw_email)
    result = {}
    result['to'] = email.utils.parseaddr(email_message['To'])
    result['from'] = email.utils.parseaddr(email_message['From'])
    result['subject'] = email_message['Subject']
    result['headers'] = email_message.items()
    result['text'] = _extract_text(email_message)
    return result


def _extract_text(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()


def process_event(evt):
    """
    We dequeue from PendingOpen and process each record.

    That means:

    1. Check against dx.doi.org for the canonical resource
    2. Scan the canonical resource for all email addresses
    3. Check if any of them match against the sender email
    4. On match:
        a) set a verification secret on PendingOpen
        b) send back a reply email asking the author to verify that
           this is the correct link
    5. On click, we need to create the OpenDocument record
    """

    # 1. check again dx.doi.org

    doi = ''.join(evt.subject.split()[2:])

    url = "http://data.crossref.org/%s" % doi
    headers = {'Accept': "application/json"}
    r = requests.get(url, headers=headers)
    jdata = json.loads(r.text)
    canon_url = jdata['feed']['entry']['pam:message']['pam:article']['prism:url']

    possible_emails = load_page(canon_url)

    if evt.sender_email in possible_emails or \
       'victor@crankycoder.com' in evt.sender_email:  # This is a debug option obviously
        # Success!, send the confirmation email back to the original
        # sender and make
        evt.verification_secret = hashlib.sha256("%x" % random.getrandbits(60 * 8)).hexdigest()
        evt.save()

        tmpl = get_template("open_confirmation_email.txt")

        url = settings.HOSTNAME + reverse("demo:add_doc", kwargs={'secret':  evt.verification_secret})
        msg = tmpl.render(Context({'doi': doi, 'add_doc_link': url}))

        send_mail("Your document is about to be added to the OAButton",
                  msg,
                  'oabutton@crankycoder,com',
                  [evt.sender_email],
                  fail_silently=False)
    else:
        # No author email match available.
        # Send an email back to the sender that the request was
        # rejected, flag the record

        # TODO: throttle mails to the user in the case of forged
        # sender address
        # TODO: generate a rejected open DOI email template with
        # mailchimp
        tmpl = get_template("rejected_open_doi.txt")

        msg = tmpl.render(Context({'doi': doi, 'canon_url': canon_url}))

        send_mail("Your submission was not accepted",
                  msg,
                  'oabutton@crankycoder,com', [evt.sender_email],
                  fail_silently=True)

        evt.rejected = True
        evt.save()
