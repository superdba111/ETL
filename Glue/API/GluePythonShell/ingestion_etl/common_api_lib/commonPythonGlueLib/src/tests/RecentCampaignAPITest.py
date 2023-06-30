import unittest


class MyTestCase(unittest.TestCase):


    def setUp(self) -> None:
        self.token = self.generate_access_token()
        self.key_list = self.get_recent_campaigns()

    def generate_access_token(self):
        import requests

        zoho_client_id = ""
        zoho_client_secret = ""
        zoho_refresh_token = ""
        redirect_uri = 'http://opsguru.io/testnothing'
        zoho_email = "fuat.arslan@e.inc"

        url = "https://accounts.zoho.com/oauth/v2/token"

        payload = f'grant_type=refresh_token&refresh_token={zoho_refresh_token}&client_id={zoho_client_id}&client_secret={zoho_client_secret}'

        print("make post request to obtain token")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_response = response.json()
        token = json_response["access_token"]
        print("Completed access token extraction")
        return token

    def get_recent_campaigns(self):
        import requests
        import json

        url = "https://campaigns.zoho.com/api/v1.1/recentcampaigns"

        headers = {
            "Authorization": f"Zoho-oauthtoken {self.token}"
        }

        parameters = {
            "resfmt": "json"
        }
        from datetime import datetime
        dt = datetime.today()
        data = requests.get(url=url, headers=headers, params=parameters)
        #print(data.text)
        data = data.json()["recent_campaigns"]
        json_data = json.dumps(data)
        # from commonPythonGlueLib.src.aws.s3.S3BucketService import S3BucketService
        # s3BucketService = S3BucketService(bucket_name='einc-og-poc-testing')
        # s3BucketService.write_to_s3(json_data, f"zohocampaigns/recentcampaigns/{dt}.json")

        keys = json.loads(json_data)
        key_list = []
        for j in keys:
            a = []
            key_list.append(j["campaign_key"])
            print("campaign key:")
            print(j["campaign_key"])
        return key_list



    def test_something(self):
        print(len(self.key_list))
        self.assertEqual(len(self.key_list), 246)


    def test_get_getcampaign_details(self):

        import requests
        import json

        url = "https://campaigns.zoho.com/api/v1.1/getcampaigndetails"

        headers = {
            "Authorization": f"Zoho-oauthtoken {self.token}"
        }

        keys = self.key_list

        for j in keys:
            # print(type(j))
            # print(j)
            parameters = {
                "resfmt": "JSON",
                "campaignkey": f"{j}",
                "campaigntype": "abtesting"
            }
            data = requests.get(url=url, headers=headers, params=parameters)
            #json_data = json.dumps(data)
            data.encoding = 'utf-8'
            json_load = data.json()   #.loads(data)
            # print(len(json_load))
            # print(json_load)

#            print(json_load['useragentstats']) ##
            useragentstats_data = None
            useragentstats_key = 'useragentstats'
            if (self.has_key(useragentstats_key, json_load)):
                useragentstats_data = json_load['useragentstats']
                print(type(useragentstats_data))
            code_data = None
            code_key = 'code'
            if (self.has_key( code_key, json_load)):
                code_data = json_load['code']
                print(code_data)
            campaign_details_data = None
            campaign_details_key = 'campaign-details'
            if (self.has_key(campaign_details_key, json_load)):
                campaign_details_data = json_load['campaign-details']
                print(campaign_details_data)
            associated_mailing_lists_data = None
            associated_mailing_lists_key = 'associated_mailing_lists'
            if (self.has_key(associated_mailing_lists_key, json_load)):
                associated_mailing_lists_data = json_load['associated_mailing_lists']
                print(associated_mailing_lists_data)
            version_data = None
            version_key = 'version'
            if (self.has_key(version_key, json_load)):
                version_data = json_load['version']
                print(version_data)
            url_data = None
            url_key = 'url'
            if (self.has_key(url_key, json_load)):
                url_data = json_load['url']
                print(url_data)
            campaign_reports_data = None
            campaign_reports_key = 'campaign-reports'
            if (self.has_key(campaign_reports_key, json_load)):
                campaign_reports_data = json_load['campaign-reports']
                print(campaign_reports_data)
            campaign_reach_data = None
            campaign_reach_key = 'campaign-reach'
            if (self.has_key(campaign_reach_key, json_load)):
                campaign_reach_data = json_load['campaign-reach']
                print(campaign_reach_data)
            campaign_status_data = None
            campaign_status_key = 'campaign_status'
            if (self.has_key(campaign_status_key, json_load)):
                campaign_status_data = json_load['campaign_status']
                print(campaign_status_data)
            segments_info_data = None
            segments_info_key = 'segments_info'
            if (self.has_key(segments_info_key, json_load)):
                segments_info_data = json_load['segments_info']
                print(segments_info_data)
            campaign_by_location_data = None
            campaign_by_location_key = 'campaign-by-location'
            if (self.has_key(campaign_by_location_key, json_load)):
                campaign_by_location_data = json_load['campaign-by-location']
                print(campaign_by_location_data)
            total_subscribers_count_data = None
            total_subscribers_count_key = 'total_subscribers_count'
            if (self.has_key(total_subscribers_count_key, json_load)):
                total_subscribers_count_data = json_load['total_subscribers_count']
                print(type(total_subscribers_count_data))
            status_data = None
            status_key = 'status'
            if (self.has_key(status_key, json_load)):
                status_data = json_load['status']
                print(type(status_data))
            # for i in json_load:
            #     print(len(i))
            #     print(i)
            print('****************')

    def has_key(self,key, json_load):
        if 'useragentstats' in json_load:
            return True
        else:
            return False



if __name__ == '__main__':
    unittest.main()
