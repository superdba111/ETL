import unittest, json, os
import pandas as pd
from commonPythonGlueLib.src.transform.RawToDF import RawToDF
from commonPythonGlueLib.src.transform.TableProps import TableProps


class RawToDFTest(unittest.TestCase):

    def setUp(self) -> None:
        self.rename_cols = TableProps(path='../resources/netsuite/tables_props.yml')
        self.row_to_df = RawToDF
        self.abs_path = os.path.abspath('../resources/department.json')
        with open(self.abs_path, 'r') as f:
            self.data = json.load(f)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('display.width', 2000)
        pd.set_option('display.float_format', '{:20,.2f}'.format)
        pd.set_option('display.max_colwidth', None)

    def test_rename_mapped_columns(self):

        flatten_json_data = self.row_to_df.get_flatten_json_data(self.data['items'])
        df = self.row_to_df.convert_json_to_df(flatten_json_data)
        actual_rename_mapping_cols = self.rename_cols.get_mapped_columns("department")
        renamed_df = self.row_to_df.rename_mapped_columns(df=df, column_map=actual_rename_mapping_cols)

        # add ingestion date as partition date
        renamed_df['partition_date'] = pd.to_datetime('today').strftime("%Y%m%d")

        self.assertIn("include_children", renamed_df.columns, "the column should be present and renamed")
        self.assertIn("external_id", renamed_df.columns, "the column should be present and renamed")
        self.assertIn("testcolumn", renamed_df.columns, "the column should be present and renamed")

    def test_get_flatten_json_data(self):
        flatten_json_data = self.row_to_df.get_flatten_json_data(self.data['items'])
        self.assertEqual(5, len(flatten_json_data), "size of records should be 5")

    def test_drop_columns(self):
        flatten_json_data = self.row_to_df.get_flatten_json_data(self.data['items'])
        df = self.row_to_df.convert_json_to_df(flatten_json_data)
        actual_rename_mapping_cols = self.rename_cols.get_mapped_columns("department")
        renamed_df = self.row_to_df.rename_mapped_columns(df=df, column_map=actual_rename_mapping_cols)
        dropped_columns_df = self.row_to_df.drop_columns(renamed_df, self.rename_cols.get_drop_columns('currency'))
        # print(dropped_columns_df.columns)
        self.assertNotIn('links', dropped_columns_df.columns, "Links column should be dropped")

    def test_dataframe_concat(self):

        flatten_json_data = self.row_to_df.get_flatten_json_data(self.data['items'])
        df = self.row_to_df.convert_json_to_df(flatten_json_data)
        actual_rename_mapping_cols = self.rename_cols.get_mapped_columns("department")
        renamed_df = self.row_to_df.rename_mapped_columns(df=df, column_map=actual_rename_mapping_cols)

        test_col_list = self.rename_cols.get_dest_columns("department") + ['test_col']
        empty_df = pd.DataFrame(columns=test_col_list)
        renamed_df = renamed_df.drop(columns=['links'])
        new_df = pd.concat([renamed_df, empty_df])

        self.assertIn('test_col', new_df.columns, ' test_col is expected in the final df')
        self.assertIn('include_children', new_df.columns, ' include_children is expected in the final df')


if __name__ == '__main__':
    unittest.main()
