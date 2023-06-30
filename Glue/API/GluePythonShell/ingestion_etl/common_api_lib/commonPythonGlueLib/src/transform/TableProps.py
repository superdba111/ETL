
import yaml
import os

class TableProps:


    def __init__(self, source_name):

        abs_path = os.path.dirname(os.path.abspath(__file__))
        print(f"Reading properties file for source {source_name}")
        prop_path = abs_path.strip().replace('transform', f'resources/{source_name}/tables_props.yml')
        with open(prop_path, 'r') as file:
            self.yaml_file = yaml.safe_load(file)


    def get_mapped_columns(self, table_name):
        column_map = {src_col: dest_col for src_col, dest_col in zip(self.yaml_file[table_name]["src_columns"], self.yaml_file[table_name]['dest_columns']) }
        return column_map

    def get_built_in_columns(self, table_name):
        built_in_col_list = self.yaml_file[table_name]["select_built_in_src_columns"]
        return ','.join([str(col) for col in built_in_col_list])

    def get_drop_columns(self, table_name):
        drop_col_list = self.yaml_file[table_name]["drop_columns"]
        return drop_col_list

    def get_src_columns(self, table_name):
        src_col_list = self.yaml_file[table_name]["src_columns"]
        return src_col_list

    def get_dest_columns(self, table_name):
        dest_col_list = self.yaml_file[table_name]["dest_columns"]
        return dest_col_list

    def get_dtypes_columns(self, table_name):
        dtypes_list = self.yaml_file[table_name]["dtypes"]
        return dtypes_list

    def get_mode(self, table_name):
        mode = self.yaml_file[table_name]["mode"]
        return mode

    def get_last_update_column(self, table_name):
        lastupdatecolumn = self.yaml_file[table_name]["lastupdatecolumn"]
        return lastupdatecolumn

    def get_start_date(self, table_name):
        start_date = self.yaml_file[table_name]["start_date"]
        return start_date

    def get_end_date(self, table_name):
        end_date = self.yaml_file[table_name]["end_date"]
        return end_date

    def get_primary_keys(self, table_name):
        return self.yaml_file[table_name]["primary_keys"]


    def get_dayforce_option_value_columns(self, table_name):
        option_value_col_list = self.yaml_file[table_name]["option_value_columns"]
        return option_value_col_list

    def get_dayforce_properties_columns(self, table_name):
        property_col_list = self.yaml_file[table_name]["employee_properties_columns"]
        return property_col_list

    def get_json_dest_columns(self, table_name):
        json_dest_col_list = self.yaml_file[table_name]["json_dest_columns"]
        return json_dest_col_list

    def get_parquet_dest_columns(self, table_name):
        parquet_dest_col_list = self.yaml_file[table_name]["parquet_dest_columns"]
        return parquet_dest_col_list




