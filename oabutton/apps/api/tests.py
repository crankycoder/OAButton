"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from oabutton.apps.api.scrapers import process_event
from oabutton.apps.api.models import PendingOpen

class SimpleTest(TestCase):
    fixtures = ['inbound.json']
    def test_read_inbound_mail(self):
        """
        Read an inbound email from IMAP,
        Extract a 3-tuple of data:

        (author_email, DOI, and open access URL)
        """
        for evt in PendingOpen.objects.all():
            process_event(evt)

#    def test_inbound_webcall():
#        """
#        We support people calling into the OAButton over an API call
#        """
#
#
#    def test_verify_email_from_doi_lookup():
#        """
#        A request to publish an open access version of a document will
#        contain a 3-tuple:
#
#        (author_email, DOI, openaccess_url)
#
#        This test should verify that the author email matches at least one
#        email address on the canonical DOI lookup
#        """
#        raise NotImplementedError
#
#    def test_open_doi_spam_protection():
#        """
#        TODO: we need to prevent spamming authors for open access versions
#        """
#        raise NotImplementedError
#
#
#    def test_notify_blocked_users():
#        """
#        Each blocked user should get a notice *once* that the document has
#        been opened.
#        """
#        raise NotImplementedError
#
#    def test_bookmarklet_shows_openaccess_version():
#        '''
#        The 3rd panel of the bookmarklet should retrieve the link to the
#        open access version of the document.
#        '''
#        pass
