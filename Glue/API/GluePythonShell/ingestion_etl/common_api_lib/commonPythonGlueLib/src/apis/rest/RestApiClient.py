import json
import datetime
import requests
import logging
import base64
import time
import jwt  # PyJWT

class RestApiClient:
    """Generic REST api ingestion class"""

    def get_request(self, url, headers):
        """
        Performs GET request on given URL

        Parameters
        ----------
        url : url to be called
        headers : additional HTTP GET headers

        Returns
        ----------
        requests_response:Request response of GET call
        """
        return requests.get(url=url, headers=headers)

    def post_request(self, url, body, headers):
        """
        Performs POST request to given URL

        Parameters
        ----------
        url : url to be called
        body : POST request body
        headers : additional HTTP GET headers

        Returns
        ----------
        requests_response:Request response of POST call
        """
        return requests.post(url, json=body, headers=headers)

    def get_basic_auth(self, user, password):
        """
        Get base64 encoded value

        Parameters
        ----------
        user : username
        password : password

        Returns
        ----------
        String:Encoded value
        """
        data = f"{user}:{password}"
        return base64.b64encode(data.encode()).decode()

    def getNetSuiteAccessToken(self, secrets):
        """
        Get Netsuite Access Token

        Parameters
        ----------
        secrets : secrets

        Returns
        ----------
        Json Response: access Token
        """
        # vars
        certificate_id = secrets["netsuite_certificate_id"]
        client_id = secrets["netsuite_client_id"]
        auth_key = secrets["netsuite_auth_key_b64"]
        account_id = secrets["netsuite_account_id"]
        iat = round(time.time(), 3)
        netsuite_url = f"https://{account_id}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token."
        decoded_auth_key = base64.b64decode(auth_key)
        encoded_jwt = jwt.encode(
            headers={
                "kid": certificate_id,
                "typ": "JWT",
                "alg": "PS256"
            },
            key=decoded_auth_key,
            payload={
                "iss": client_id,
                "scope": "rest_webservices",
                "aud": netsuite_url,
                "iat": iat,
                "exp": iat + 3600
            }
        )

        init_url = f"https://{account_id}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        params = {
            'grant_type': 'client_credentials',
            'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
            'client_assertion': encoded_jwt
        }
        response = requests.request("POST", init_url, headers=headers, params=params)
        response.encoding = 'utf-8'
        respone_json = response.json()
        token = respone_json["access_token"]

        return token

    def getNetsuiteJdbcAccessToken(self, secrets):
        """
        Get Netsuite JDBC SuiteAnalytics Access Token

        Parameters
        ----------
        secrets : secrets

        Returns
        ----------
        Json Response: access Token
        """
        # vars
        certificate_id = secrets["netsuite_certificate_id"]
        client_id = secrets["netsuite_client_id"]
        auth_key = secrets["netsuite_auth_key_b64"]
        account_id = secrets["netsuite_account_id"]
        grant_type = "client_credentials"

        client_assertion_type = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
        token_endpoint_url = f"https://{account_id}.suitetalk.api.netsuite.com/services/rest/auth/oauth2/v1/token"
        connect_endpoint_url = f"https://{account_id}.connect.api.netsuite.com/services/rest/auth/oauth2/v1/token"
        scopes = ['SuiteAnalytics']
        private_key = base64.b64decode(auth_key)

        iat = round(time.time(), 3)
        payload = {
            'iss': client_id,
            'scope': scopes,
            'aud': connect_endpoint_url,
            'iat': iat,
            'exp': iat + 3600
        }

        jwt_assertion = jwt.encode(payload, private_key, algorithm="PS256", headers={'kid': certificate_id})

        data = {
            'grant_type': grant_type,
            'client_assertion_type': client_assertion_type,
            'client_assertion': jwt_assertion,
        }
        resp = requests.post(token_endpoint_url, data=data)
        data = resp.json()
        logging.debug("Received '%s'[%d]: %s", token_endpoint_url, resp.status_code, resp.raw)

        assert data["access_token"]

        access_token = data["access_token"]

        return access_token

    def getNetSuiteRequest(self, secrets, built_in_columns, table, token,limit, condition='', offset=0):
        """
        Get API calls for data ingestion

        Parameters
        ----------
        secrets : aws secrets
        built_in_columns : column names for select statements
        table: table name
        token: API token
        limit: API limit response
        condition: filter condition
        offset: pagination index

        Returns
        ----------
        response: json response of API
        """
        account_id = secrets["netsuite_account_id"]
        url = f"https://{account_id}.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql?limit={limit}&offset={offset}"

        full_query = self._get_query(table, built_in_columns, condition)
        payload = json.dumps({
            "q": full_query
        })
        headers = {
            'Content-Type': 'application/json',
            'prefer': 'transient',
            'Authorization': f'Bearer {token}',
            'Cookie': 'NS_ROUTING_VERSION=LAGGING'
        }
        print(f"Url request: {url}")
        print(f"Query: {full_query}")
        response = requests.request("POST", url, headers=headers, data=payload)
        if (response.status_code == 200):
            response.encoding = 'utf-8'
            return response.json(),200
        else:
            print(f"API Invocation Issue Requeset: {response}\n {response.text}")
            return None,response.status_code

    def _get_query(self, table, built_in_columns="", condition=""):
        """
        Helper Method
        """
        full_query = f"SELECT * FROM {table}"
        if(table == 'invoice_data'):
            full_query = f"""SELECT {built_in_columns} FROM Transaction
                                     INNER JOIN Entity ON( Entity.ID = Transaction.Entity ) 
                                     LEFT OUTER JOIN Employee ON ( Employee.ID = Transaction.Employee ) 
                                     INNER JOIN TransactionLine ON ( TransactionLine.Transaction = Transaction.ID )
                                     WHERE ( Transaction.TranDate = TO_DATE('2020-12-01', 'YYYY-MM-DD' ) ) 
                                     AND ( TransactionLine.MainLine = 'T' )"""
        else:
            if(condition):
                full_query = f"SELECT {built_in_columns} FROM {table} {condition}"
            else:
                full_query = f"SELECT {built_in_columns} FROM {table}"
        return full_query

    def getZohoCampaignAccessToken(self, secrets, token_url ):


        zoho_client_id = secrets["zoho_client_id"]
        zoho_client_secret = secrets["zoho_client_secret"]
        zoho_refresh_token = secrets["zoho_refresh_token"]

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

    def getZohoAccessToken(self, secrets):
        """
        Zoho CRM Access Token

        Parameters
        ----------
        secrets : secrets

        Returns
        ----------
        Json Response: access Token
        """
        init_url = "https://accounts.zoho.com/oauth/v2/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        client_id = secrets['zoho_client_id']
        client_secret = secrets['zoho_client_secret']
        refresh_token = secrets['zoho_refresh_token']
        # redirect_uri = secrets['redirect_uri']
        # zoho_email = secrets['zoho_email']

        payload = {
            "grant_type": "refresh_token",
            "client_secret": f"{client_secret}",
            "client_id": f"{client_id}",
            "refresh_token": f"{refresh_token}"
        }
        response = requests.request("POST", init_url, data=payload, headers=headers)
        response.encoding = 'utf-8'
        respone_json = response.json()
        token = respone_json["access_token"]

        return token

    def getDayForceAccessToken(self,secrets,token_api_url):
        """
        Get Dayforce Access Token

        Parameters
        ----------
        secrets :  secrets from AWS secrets manager
        token_api_url : environment specific url for access token
        """
        company_id = secrets["dayforce_company_id"]
        password = secrets["dayforce_password"]
        username = secrets["dayforce_username"]

        payload = {
            "grant_type": "password",
            "companyId": company_id,
            "username": username,
            "password": password,
            "client_id": "Dayforce.HCMAnywhere.Client"
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST",
                                    token_api_url,
                                    data=payload,
                                    headers=headers)
        response.encoding = 'utf-8'
        response_json = response.json()

        if str(response.status_code).strip() != "200":
            print("Authentication error: " + " - " + str(response.status_code) + " - " + str(response.reason))
            raise Exception("Authentication error: " + " - " + str(response.status_code))
        token = response_json["access_token"]
        print("Token extracted successfully")

        return token
    def createRestBulkEmployeeJob(self, xref_string, token, bulk_url, expanders):
        """
        Get API calls for data ingestion

        Parameters
        ----------
        expanders: additional columns to add based on documentation
        xref_string: List of xrefs to pull as a single string comma separated
        Returns
        ----------
        response: json response of API
        """
        url = bulk_url
        payload = json.dumps({
            "EmployeeXRefCode": xref_string,
            "Expand": expanders
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        params = {
            "isValidateOnly":"true"
        }
        print(f"Url request: {url}")
        response = requests.request("POST", bulk_url,
                                    headers=headers,
                                    data=payload,
                                    params=params)
        response.encoding = 'utf-8'
        response_json = response.json()['Data']['JobStatus']
        json_object = json.dumps(response_json)
        # if (response.status_code == 200):
        #     response.encoding = 'utf-8'
        #     return response.json(),200
        # else:
        #     print(f"API Invocation Issue Requeset: {response}\n {response.text}")
        #     return None,response.status_code
        print("Job status")
        while True:
            status_response = requests.request("GET",
                                               response_json,
                                               headers=headers)
            status = status_response.json()['Data']['Status']
            if status == 'Received':
                print(status + " as of : " + str(datetime.datetime.now()))
            else:
                if status != 'Succeeded':
                    print("Beyond received but not there yet")
                    print(status + " as of : "+ str(datetime.datetime.now()))
                else:
                    print("Succeeded at : " + str(datetime.datetime.now()))
                    file_url = status_response.json()['Data']['Results']
                    break
            time.sleep(5)
        data = requests.request("GET",
                                file_url,
                                headers=headers)
        json_out = data.json()['Data']
        print("Initial Count of records")
        print(len(json_out))
        pagination = data.json()['Paging']['Next']
        paging = True
        while paging:
            print(pagination)
            if pagination.strip() != "":
                print("Extract additional records")
                pagination_request = requests.request("GET", pagination, headers=headers).json()
                pagination_json = pagination_request['Data']
                print("add additional " + str(len(pagination_json)) + "records")
                print(type(pagination_json))
                print(type(json_out))
                json_out = json_out + pagination_json
                print(len(json_out))
            else:
                print("no more pagination")
                paging = False
                break
            pagination = pagination_request['Paging']['Next']
        return json_out
    def getDayForceEmployeeXrefs(self, token, employee_url):

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        response = requests.request("GET", url=employee_url, headers=headers)
        if str(response.status_code).strip() != "200":
            print("Authentication error: " + " - " + str(response.status_code) + " - " + str(response.reason))
            raise Exception("Authentication error: " + " - " + str(response.status_code))
        xref_list_raw = response.json()['Data']
        xref_list_out = []
        for x in xref_list_raw:
            xref_list_out.append(x['XRefCode'])
        xref_string_output = str('"' + ','.join(xref_list_out) + '"')
        return xref_string_output

    def getDayForceEmployeePayrollSummaryData(self, token, pay_summary_api_url, start_date, end_date):

        headers = {
            'Content-Type': 'application/json',
            'prefer': 'transient',
            'Authorization': f'Bearer {token}',
            'Cookie': 'NS_ROUTING_VERSION=LAGGING'
        }
        print(headers)
        parameters = {
            "filterPaySummaryStartDate" : start_date,
            "filterPaySummaryEndDate" : end_date
        }
        print(parameters)

        response = requests.request(method="GET",url=pay_summary_api_url, headers=headers, params=parameters)
        if str(response.status_code).strip() != "200":
            print("Authentication error: " + " - " + str(response.status_code) + " - " + str(response.reason))
            raise Exception("Authentication error: " + " - " + str(response.status_code))
        response_json = response.json()
        output_json = []
        output_json = output_json + (response_json['Data'])
        print("1st response")
        headers = {
            'Content-Type': 'application/json',
            'prefer': 'transient',
            'Authorization': f'Bearer {token}',
            'Cookie': 'NS_ROUTING_VERSION=LAGGING'
        }
        Paging = True
        while Paging:
            if 'Data' in response_json:
                print("Some data recieved")
                #        output_json = output_json + json['Data']
                Paging_url = response_json['Paging']['Next']
                print(Paging_url)

                if Paging_url.strip() != "":
                    print("Extracting next page of data")
                    response = requests.request("GET", url=Paging_url, headers=headers)
                    response_json = response.json()
                    if 'Data' in response_json:
                        print("append data")
                        output_json = output_json + (response_json['Data'])
                        #Paging_url = response_json['Paging']['Next']
                    else:
                        print("Finished load with final request")
                else:
                    print("No more pages left to request")
                    Paging = False

            else:
                Paging = False
        return output_json