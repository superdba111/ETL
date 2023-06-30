import json
from datetime import datetime

from zcrmsdk.src.com.zoho.crm.api.modules import *



# from get_modules import Module



from zcrmsdk.src.com.zoho.crm.api.query import *


class Query(object):

    
    # def __init__(self, sdkInitializer):
    #     sdkInitializer.initialize()


    @staticmethod
    def get_records(query):

        """
        This method is used to get records from the module through a COQL query.
        """
        # Get instance of QueryOperations Class
        query_operations = QueryOperations()

        # Get instance of BodyWrapper Class that will contain the request body
        body_wrapper = BodyWrapper()

        select_query = query

        body_wrapper.set_select_query(select_query)

        # Call get_records method that takes BodyWrapper instance as parameter
        response = query_operations.get_records(body_wrapper)
        response.encoding = "UTF-8"
        record_list_json = []
        if response is not None:

            # Get the status code from response
            print('Status Code: ' + str(response.get_status_code()) + ' - fine up to line 477')

            if response.get_status_code() in [204, 304]:
                print('No Content' if response.get_status_code() == 204 else 'Not Modified')
                return

            # Get object from response
            response_object = response.get_object()

            if response_object is not None:

                # Check if expected ResponseWrapper instance is received.
                if isinstance(response_object, ResponseWrapper):

                    # Get the list of obtained Record instances
                    record_list = response_object.get_data()



                    for record in record_list:

                        # print("FULL RECORD")

                        jsonStr = json.dumps(record.__dict__)
                        strJson = json.loads(str(jsonStr))

                        print(strJson)
                        # print(strJson['_Record__key_values'])
                        record_list_json.append(strJson['_Record__key_values'])

                    #print(record_list_json)

                # Check if the request returned an exception
                elif isinstance(response_object, APIException):
                    # Get the Status
                    print("Status: " + response_object.get_status().get_value())

                    # Get the Code
                    print("Code: " + response_object.get_code().get_value())

                    print("Details")

                    # Get the details dict
                    details = response_object.get_details()

                    for key, value in details.items():
                        print(key + ' : ' + str(value))

                    # Get the Message
                    print("Message: " + response_object.get_message().get_value())
        return record_list_json


#sdkInitializer = SDKInitializer

