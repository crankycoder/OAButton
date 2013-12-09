from django.test import TestCase
from oabutton.phantomjs.grab_page import load_page

class LoadURLTest(TestCase):
    def test_load_javascript_scrambled_emails(self):
        url = "http://stke.sciencemag.org/cgi/content/abstract/sigtrans;6/302/ra100"
        emails = load_page(url)
        assert "gelvin@purdue.edu" in emails
