from django.db import models


class OAApiKey(models.Model):
    owner_email = models.EmailField(db_index=True, null=False)
    api_key = models.TextField(max_length=40, null=False)

    date_requested = models.DateTimeField(auto_now=True)
    verification_secret = models.TextField(max_length=40, null=False)

    date_enabled = models.DateTimeField(auto_now=False)

class PendingOpen(models.Model):
    """
    These are requests that need to be processed into OpenDocument.

    We need to grab the DOI, scan for an email address
    """
    sender_email = models.EmailField(db_index=True, null=False)
    subject = models.TextField(max_length=2000)
    email_text = models.TextField(max_length=4000)
    email_headers = models.TextField(max_length=4000, null=False, default="")

    verification_secret = models.TextField(max_length=80, null=False, db_index=True)

    rejected = models.BooleanField(default=False)

class OpenDocument(models.Model):
    doi = models.TextField(max_length=2000)

    oa_url = models.URLField(max_length=2000)

    release_email = models.EmailField(db_index=True, null=False)

    date_opened = models.DateTimeField()

    # Presumably, we'd be able to get some kind of canonical
    # repository for papers that comply with immediate deposit
    # mandate.
    # Details:
    #   http://openaccess.eprints.org/index.php?/archives/249-OA-Mandates,-Embargoes,-and-the-Fair-Use-Button.html
    #   http://openscience.com/green-open-access-on-the-move/
    # We should probably add that here
