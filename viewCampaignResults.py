#!/usr/bin/python3

from templateGenerator import TemplateGenerator


template = TemplateGenerator("viewCampaignResults")

variables = dict()
variables['WEBSITE_TITLE'] = "Spear Phishing Control Panel"
variables['PAGE_HEADING'] = "Viewing Campaign Results"
variables['PAGE_SCRIPTS'] = "<script src=\"getCampaignResults.js\"></script>"
variables['PAGE_ONLOAD'] = "onload=\"when_loaded();\""

template.parse(variables)
