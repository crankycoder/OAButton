# Create your views here.
from models import PendingOpen
from datetime import datetime
from django.shortcuts import render_to_response

def add_doc(req, secret):

    for pending in PendingOpen.objects.filter(verfication_secret = secret):
        for l in pending.email_text.split('\n'):
            if l.strip().startswith("http"):
                url = l.strip()

                # Extract the DOI, this should've been done before
                # creating the PendingOpen object
                doi = ''.join(evt.subject.split()[2:])

                # TODO: verify that the URL we're adding is
                # actually live

                OpenDocument.objects.create(doi=doi, oa_url=url,
                        release_email = evt.sender_email,
                        date_opened=datetime.now())

                evt.delete()

                # TODO: add document open success
                return render_to_response('api/document_open_success.html')

    # TODO: add document open failure template
    return render_to_response('api/document_open_fail.html')

