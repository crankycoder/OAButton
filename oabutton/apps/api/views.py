# Create your views here.
from models import PendingOpen
from datetime import datetime

def add_doc(req, secret):
    results = PendingOpen.objects.filter(verfication_secret = secret)
    if len(results) > 0:
        for evt in results:
            for l in evt.email_text.split('\n'):
                if l.strip().startswith("http"):
                    url = l.strip()
                    doi = ''.join(evt.subject.split()[2:])

                    # TODO: verify that the URL we're adding is
                    # actually live

                    OpenDocument.objects.create(doi=doi, oa_url=url,
                            release_email = evt.sender_email,
                            date_opened=datetime.now())

                    evt.delete()
