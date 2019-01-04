import pprint
from jinja2 import Template
from mailchimpapi import MailchimpAPI
from datetime import datetime
import os
from BiblePassageReference import BiblePassageReference
import csv
import json
from BibleGatewayScraper import BibleGatewayScraper
import sys


if 'MAILCHIMP_API_KEY' not in os.environ.keys():
    print("MAILCHIMP_API_KEY environment variable required to talk to mailchimp.")
    exit(1)

MAILCHIMP_API_KEY = os.environ['MAILCHIMP_API_KEY']

if len(sys.argv) != 2:
    print("Expecting config file to be specified")
    exit(1)

config_file_path = sys.argv[1]

if not os.path.isfile(config_file_path):
    print("Config file ({}) required to continue.".format(config_file_path))
    exit(1)

with open(config_file_path) as config_file:
    config = json.load(config_file)

if 'mailchimp' not in config and 'enabled' not in config['mailchimp']:
    print("missing config mailchimp/enabled")
    exit(1)
mailchimp_enabled = config['mailchimp']['enabled']

if 'mailchimp' not in config and 'list_id' not in config['mailchimp']:
    print("missing config mailchimp/list_id")
    exit(1)
target_list_id = config['mailchimp']['list_id']

if 'mailchimp' not in config and 'campaign_folder' not in config['mailchimp']:
    print("missing config mailchimp/campaign_folder")
    exit(1)
campaign_folder_name = config['mailchimp']['campaign_folder']

if 'mailchimp' not in config and 'subject_prefix' not in config['mailchimp']:
    print("missing config mailchimp/subject_prefix")
    exit(1)
subject_prefix = config['mailchimp']['subject_prefix']

if 'mailchimp' not in config and 'from_email' not in config['mailchimp']:
    print("missing config mailchimp/from_email")
    exit(1)
from_email = config['mailchimp']['from_email']

if 'mailchimp' not in config and 'from_name' not in config['mailchimp']:
    print("missing config mailchimp/from_name")
    exit(1)
from_name = config['mailchimp']['from_name']

if 'facebook_link' not in config:
    print("missing config facebook_link")
    exit(1)
facebook_link = config['facebook_link']

scraper = BibleGatewayScraper('https://www.biblegateway.com')
mailchimp = MailchimpAPI(MAILCHIMP_API_KEY)

reading_plan = []

reading_plan_file = config['plan']['file']

print("Parsing the reading plan... and fetching Bible text")

now = datetime.now()

def decomment(csvfile):
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw: yield raw

with open(reading_plan_file) as csv_file:
    plan_reader = csv.reader(decomment(csv_file), delimiter=',', quotechar='"')
    for row in plan_reader:
        date_string, reading = row
        date = datetime.strptime(date_string, "%d/%m/%Y %H:%M:%S")

        passage_reference = BiblePassageReference.parse(reading)

        print(str(date) + " - " + passage_reference.pretty())

        if date < now:
            print("Date is in the past - skipping.")
            continue

        text = scraper.get_passage_by_reference(passage_reference, version="NIVUK")

        reading_plan.append({'time_to_send': date, "passage_reference": passage_reference, 'text': text})

folder_id = mailchimp.create_campaign_folder(campaign_folder_name)

basic_campaign_definition = {
    'type': 'regular',
    'recipients': {
        'list_id': target_list_id
    },
    'settings': {
        'from_name': from_name,
        'reply_to': from_email,
        'folder_id': folder_id
    },
    'tracking': {
        'opens': True,

    }
}

with open('email_template.html.j2', 'r') as template_file:
    template_string = template_file.read()

daily_reading_email_template = Template(template_string)

for daily_reading in reading_plan:
    nice_date_string = daily_reading['time_to_send'].strftime('%A %d %B')

    rendered_email_html = daily_reading_email_template.render(passage_title=daily_reading['passage_reference'].pretty(),
                                                              text=daily_reading['text'],
                                                              date_string=nice_date_string,
                                                              facebook_link=facebook_link
                                                              )

    file_name = "email." + daily_reading['time_to_send'].isoformat() + '.' + daily_reading[
        'passage_reference'].__repr__() + '.html'
    print(file_name)
    with open(os.path.join('./emails', file_name), "w") as email_html_file:
        email_html_file.write(rendered_email_html)

    campaign_definition = dict(basic_campaign_definition)

    subject = "{} - {}".format(subject_prefix, daily_reading['passage_reference'].pretty())

    campaign_definition['settings']['subject_line'] = subject
    campaign_definition['settings']['title'] = subject

    if mailchimp_enabled:

    	campaign_id = mailchimp.create_campaign(campaign_definition)

    	print("Campaign ID >>>>")
    	print(campaign_id)
    	print("<<<<")

    	mailchimp.set_campaign_html_text(campaign_id, rendered_email_html)

    	mailchimp.schedule_campaign_for_datetime(campaign_id, daily_reading['time_to_send'])
