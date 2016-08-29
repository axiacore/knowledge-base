#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: AxiaCore S.A.S. http://axiacore.com
from django.conf import settings
from django.utils.safestring import mark_safe

GA_CODE = """
<script>
(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');
ga('create', '%s', 'auto');
ga('send', 'pageview');
</script>
<noscript>
<iframe src="//www.googletagmanager.com/ns.html?id=%s" height="0" width="0"
style="display:none;visibility:hidden"></iframe></noscript><script>
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),
event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),
dl=l!='dataLayer'?'&l='+l:'';j.async=true;
j.src='//www.googletagmanager.com/gtm.js?id='+i+dl;
f.parentNode.insertBefore(j,f);})(window,document,'script',
'dataLayer','%s');</script>
"""


def logo_company(request):
    return {'LOGO_COMPANY': settings.LOGO_COMPANY}


def analytics(request):
    """
    Enable analytics script if debug is False
    """
    script = ''
    if not settings.DEBUG:
        script = GA_CODE % (
            settings.GOOGLE_ANALYTICS_CODE,
            settings.TAG_MANAGER_ID,
            settings.TAG_MANAGER_ID,
        )

    return {'ANALYTICS': mark_safe(script)}
