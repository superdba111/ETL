import pandas as pd

class RawToDF:

    # def __init__(self):
    #     self._df = pd.DataFrame()

    def convert_json_to_df(json):
        """
        Convert json data to DataFrame
        :param json: json input
        :return: dataframe
        """
        flattened_json = json
        df_json = pd.DataFrame(flattened_json)
        return df_json

    def get_flatten_json_data(json_data):
        """
        Flatten the nested Json Data
        :param json_data: input nasted json response
        :param table_name: table input for custom fields.
        :return: the flatten json data
        """
        flatten_json_data = []
        try:
            json_list = json_data  # ['result']

            for json_element in json_list:
                if len(json_element) > 0:
                    flatten_json = {}
                    for key in json_element:
                        flatten_json = {**flatten_json, **{str(key): str(json_element[key])}}

                    flatten_json_data.append(flatten_json)
        except Exception as e:
            print(f"Error  {e}. ")

        return flatten_json_data




    def rename_mapped_columns( df, column_map):
        # _df = pd.DataFrame()
        # _df = df
        return df.rename(columns=column_map)

    def drop_columns(df, columns):
        # _df = pd.DataFrame()
        # _df = df
        return df.drop(columns=columns, errors='ignore')

    def get_flatten_dayforce_employee_properties_data(json_data, option_value_list, properties_list):
        """
        Flatten the nested Json Data
        :param json_data: input nasted json response
        :param table_name: table input for custom fields.
        :return: the flatten json data
        """
        employeeNumber = json_data['EmployeeNumber']
        EmployeeProperties = json_data['EmployeeProperties']
        XRefCode = json_data['XRefCode']
        properties_list = ["Class", "Business Unit"]
        option_value_list = ["XRefCode","ShortName"]
        LastModifiedTimestamp = json_data['LastModifiedTimestamp']
        jsonOut = []
        if len(employeeNumber) > 0:
            for key in employeeNumber:
                flatten_json = {}
                flatten_json = {**flatten_json, "EmployeeNumber": str(employeeNumber[key])}

                if EmployeeProperties[key] is not None:
                    properties = EmployeeProperties[key]['Items']
                    for prop in properties:
                        for empproperty in properties_list:
                            if prop['EmployeeProperty']['ShortName'] == empproperty:
                                for option in option_value_list:
                                    if option == "XRefCode":
                                        flatten_json = {**flatten_json, empproperty.lower().replace(" ", "_")+ "_" + "xref_code" : str(prop['OptionValue'][option])}
                                    elif option == "ShortName":
                                        flatten_json = {**flatten_json, empproperty.lower().replace(" ", "_")+ "_" + "short_name" : str(prop['OptionValue'][option])}

                flatten_json = {**flatten_json, "XRefCode": str(XRefCode[key])}
                flatten_json = {**flatten_json, "LastModifiedTimestamp": str(LastModifiedTimestamp[key])}
                jsonOut.append(flatten_json)

        return jsonOut
    def get_flatten_dayforce_employee_status_data(json_data):
        """
        Flatten the nested Json Data
        :param json_data: input nasted json response
        :param table_name: table input for custom fields.
        :return: the flattened json data
        """
        EmployeeNumber = json_data['EmployeeNumber']
        EmploymentStatuses = json_data['EmploymentStatuses']
        EmployeeStatusList = ["LastModifiedTimestamp", "EffectiveStart","NormalWeeklyHours"]
        EmployeeStatusNestedList = ["EmploymentStatus","EmploymentStatusGroup","PayType","PayGroup","PayTypeGroup","PayClass","PayPolicy","PayHolidayGroup","EntitlementPolicy", "ShiftRotation","TimeOffPolicy","PayrollPolicy"]
        LastModifiedTimestamp = json_data['LastModifiedTimestamp']
        jsonOut = []
        if len(EmployeeNumber) > 0:
            for key in EmployeeNumber:
                flatten_json = {}
                if EmploymentStatuses[key] is not None:
                    flatten_json = {**flatten_json, "EmployeeNumber": str(EmployeeNumber[key])}
                    flatten_json = {**flatten_json, "LastModifiedTimestamp": str(LastModifiedTimestamp[key])}
                    EmploymentStatusesData = EmploymentStatuses[key]['Items']
                    for col in EmploymentStatusesData:
                        for status in EmployeeStatusNestedList:
                            if status in col:
                                print(col[status]['ShortName'])
                                flatten_json = {**flatten_json, status.lower().replace(" ", "_") : str(col[status]['ShortName'])}
                        for status in EmployeeStatusList:
                            if status in col:
                                flatten_json = {**flatten_json, status: str(col[status])}
                    jsonOut.append(flatten_json)
        return jsonOut