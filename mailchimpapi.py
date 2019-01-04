import httplib2
import json
import pprint
import urllib.parse


class MailchimpAPI:

    def __init__(self, api_token):

        _, region = api_token.split('-')

        self.base_url = 'https://{}.api.mailchimp.com/3.0'.format(region)
        self.api_token = api_token
        self.h = httplib2.Http(".cache")
        self.auth_headers = {'Authorization': 'apikey ' + self.api_token}

    def __fetch_json(self, url):
        (response, content) = self.h.request(url, "GET", headers=self.auth_headers)
        return json.loads(content)

    def __post_json(self, url, payload):
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        (response, content) = self.h.request(uri=url, method='POST', headers={**headers, **self.auth_headers},
                                             body=json.dumps(payload))

        if response['status'] != '200' and response['status'] != '204':
            print("Got Non 200 response!")
            pprint.pprint(response)
            try:
                json_content = json.loads(content)
                pprint.pprint(json_content)
            except json.decoder.JSONDecodeError:
                print(content)
            return None

        return content

    def __put_json(self, url, payload):
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        (response, content) = self.h.request(uri=url, method='PUT', headers={**headers, **self.auth_headers},
                                             body=json.dumps(payload))

        if response['status'] != '200' and response['status'] != '204':
            print("Got Non 200 response!")
            pprint.pprint(response)
            try:
                json_content = json.loads(content)
                pprint.pprint(json_content)
            except json.decoder.JSONDecodeError:
                print(content)
            return
        return

    def get_lists(self):
        url = self.base_url + "/lists"
        return self.__fetch_json(url)

    def get_list(self, list_id):
        url = self.base_url + "/lists/" + list_id
        return self.__fetch_json(url)


    def get_campaign_folders(self):
        url = self.base_url + "/campaign-folders"
        return self.__fetch_json(url)

    def create_campaign_folder(self, campaign_folder_name):

        existing_campaign_folders = self.get_campaign_folders()

        name_already_exists = any(folder['name'] == campaign_folder_name for folder in existing_campaign_folders['folders'])
        if name_already_exists:
            existing_campaign_folder = next(folder for folder in existing_campaign_folders['folders'] if folder['name'] == campaign_folder_name)
            return existing_campaign_folder['id']

        url = self.base_url + "/campaign-folders"

        payload = {"name": campaign_folder_name}

        created_campaign_folder = json.loads(self.__post_json(url, payload))
        if created_campaign_folder:
            return created_campaign_folder['id']

    def get_campaigns(self):
        url = self.base_url + "/campaigns?count=500"
        return self.__fetch_json(url)

    def get_campaign_ids_by_name(self, name):
        encoded_name = urllib.parse.quote_plus(name)
        url = self.base_url + '/search-campaigns?query=' + encoded_name
        response = self.__fetch_json(url)
        if 'results' not in response:
            return []
        real_matches = list(filter(lambda result: result['campaign']['settings']['title'] == name, response['results']))
        ids = list(map(lambda result: result['campaign']['id'], real_matches))
        return ids


    def create_campaign(self, campaign_definition):

        campaign_name = campaign_definition['settings']['title']

        existing_ids = self.get_campaign_ids_by_name(campaign_name)

        if len(existing_ids) > 1:
            print("Multiple campaigns ({}) exist with this name: {}".format(existing_ids, campaign_name))
            exit(1)

        if len(existing_ids) == 1:
            print("Campaign named {} already exists.".format(campaign_name))
            return existing_ids[0]

        print("No existing campaign named {} - creating.".format(campaign_name))

        url = self.base_url + "/campaigns"

        created_campaign = json.loads(self.__post_json(url, campaign_definition))
        if created_campaign:
            return created_campaign['id']

    def set_campaign_html_text(self, campaign_id, html_content):
        url = self.base_url + "/campaigns/" + campaign_id + "/content"

        body = {'html': html_content}

        self.__put_json(url, body)

    def send_campaign(self, campaign_id):
        url = self.base_url + '/campaigns/' + campaign_id + '/actions/send'

        response = self.__post_json(url, None)
        return response

    def schedule_campaign_for_datetime(self, campaign_id, datetime):

        url = self.base_url + '/campaigns/' + campaign_id + '/actions/schedule'

        schedule_defintion = {
            "schedule_time": datetime.isoformat(),
            "timewarp": False,
            "batch_delay": False
        }

        return self.__post_json(url, schedule_defintion)

