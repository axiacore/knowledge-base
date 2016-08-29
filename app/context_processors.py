#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: AxiaCore S.A.S. http://axiacore.com
from django.conf import settings
from django.utils.safestring import mark_safe
from string import Template


TRACKING_CODE = """
<script>
window.ga=window.ga||function(){(ga.q=ga.q||[]).push(arguments)};
ga.l=+new Date;
ga('create', '$ga_code', 'auto');
ga('send', 'pageview');
</script>
<script async src='https://www.google-analytics.com/analytics.js'></script>
"""


def logo_company(request):
    return {'LOGO_COMPANY': settings.LOGO_COMPANY}


def analytics(request):
    """
    Enable analytics script if debug is False
    """
    script = ''
    if not settings.DEBUG:
        template = Template(TRACKING_CODE)
        script = mark_safe(
            template.substitute(
                ga_code=settings.GOOGLE_ANALYTICS_CODE,
            )
        )

    return {'ANALYTICS': script}
