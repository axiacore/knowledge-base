#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: AxiaCore S.A.S. http://axiacore.com
from django.conf import settings

def logo_company(request):
	return {'LOGO_COMPANY' : settings.LOGO_COMPANY}
