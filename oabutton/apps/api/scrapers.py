import BeautifulSoup

import imaplib
import email

def check_inbox(save_callable):
    """
    Check inbound mail
    """
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('oabutton@crankycoder.com', 'hackoabutton')
    mail.select("inbox") # connect to inbox.

    result, data = mail.uid('search', None, "ALL") # search and return uids instead
    # the result should always come back with 'OK'
    uids = data[0].split()
    for msg_uid in uids:
        raw_email = load_mail_by_uid(mail, msg_uid)
        mail_dict = process_raw_email(raw_email)
        print "--------"
        print "From: %s <%s>" % mail_dict['from']
        print "To: %s <%s>" % mail_dict['to']
        print "Subject: %s" % mail_dict['subject']
        print mail_dict['text']

        # TODO: add the record
        save_callable(mail_dict)

        # Label the message as processed (only works with gmail)
        mail.uid('STORE', msg_uid, '+X-GM-LABELS', 'processed')

        # Mark the message as deleted (which is basically archived)
        mail.uid('STORE', msg_uid, '+FLAGS', '(\Deleted)')


def process_raw_email(raw_email):
    """
    Return a dictionary with the following keys:
    """
    email_message = email.message_from_string(raw_email)
    result = {}
    result['to'] = email.utils.parseaddr(email_message['To'])
    result['from'] = email.utils.parseaddr(email_message['From'])
    result['subject'] = email_message['Subject']
    result['headers'] = email_message.items() # print all headers
    result['text'] = extract_text(email_message)
    return result

def extract_text(email_message_instance):
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()


def load_mail_by_uid(mail, uid):
    """return the raw email"""
    result, data = mail.uid('fetch', uid, '(RFC822)')
    return data[0][1]

def scrape_email(html_text):
    pass

check_inbox()

