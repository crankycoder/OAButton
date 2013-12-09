# Create your views here.
from datetime import datetime
from django.conf import settings
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from models import PendingOpen, OpenDocument
import json

def inspect(req, doi):
    data = json.dumps([])
    docs = OpenDocument.objects.filter(doi=doi)
    if len(docs) > 0:
        # Grab all open documents
        data = serializers.serialize("json", docs)
    return HttpResponse(data, content_type='application/json')

def add_doc(req, secret):

    for pending in PendingOpen.objects.filter(verification_secret = secret):
        for l in pending.email_text.split('\n'):
            if l.strip().startswith("http"):
                url = l.strip()

                # Extract the DOI, this should've been done before
                # creating the PendingOpen object
                doi = ''.join(pending.subject.split()[2:])

                # TODO: verify that the URL we're adding is
                # actually live

                OpenDocument.objects.create(doi=doi, oa_url=url,
                        release_email = pending.sender_email,
                        date_opened=datetime.now())

                pending.delete()

                return render_to_response('api/document_open_success.html',
                        {'doi': doi, 'url': url, 'hostname':
                            settings.HOSTNAME, 'api_url': reverse('demo:inspect', kwargs={'doi': doi}) })

    # TODO: add document open failure template
    return render_to_response('api/document_open_fail.html')

