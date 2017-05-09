#!/usr/bin/python3
import cgi

from templateGenerator import TemplateGenerator


# Which of our many batches are we interested in?
data = cgi.FieldStorage()
batch_id = int(data['id'].value) if 'id' in data else 0

template = TemplateGenerator("viewResultDetail")

variables = dict()
variables['WEBSITE_TITLE'] = "Spear Phishing Control Panel"
variables['PAGE_HEADING'] = "Viewing Campaign Results"
variables['PAGE_SCRIPTS'] = "<script src=\"getResultsDetail.js\"></script>"
variables['PAGE_ONLOAD'] = "onload=\"when_loaded();\""
variables['BATCH_ID'] = str(batch_id)

template.parse(variables)
