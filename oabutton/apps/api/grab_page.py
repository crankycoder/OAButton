"""
This is a dirty hack, we need to add a bunch of sanitization to make
sure that people can't run arbitrary code with this
"""
from django.conf import settings
import subprocess
import re
import tempfile
from django.template import Context
from django.template.loader import get_template


def load_page(url):
    tmpl = get_template("phantomjs_loader.js")
    jscode = tmpl.render(Context({"url": url}))
    with tempfile.NamedTemporaryFile(delete=True) as tmp:
        filename = tmp.name
        tmp.write(jscode)
        tmp.flush()
        cmd = "%s %s" % (settings.PHANTOMJS_BIN, filename)
        child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        stdoutdata, stderrdata = child.communicate()
        possible_emails = set([f[0] for f in re.findall(r"(\w+@\w+(.\w+))", stdoutdata)])
        return possible_emails
    return set()
