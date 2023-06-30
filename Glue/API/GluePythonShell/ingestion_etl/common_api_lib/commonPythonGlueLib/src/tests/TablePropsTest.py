import unittest
from commonPythonGlueLib.src.transform.TableProps import TableProps


class TablePropsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.rename_cols = TableProps(source_name='netsuite')

    def test_get_mapped_columns(self):
        actual_rename_mapping_cols = self.rename_cols.get_mapped_columns("currency")
        expected_rename_mapping_cols = {
            'currencyprecision': 'currency_precision',
            'displaysymbol': 'display_symbol',
            'exchangerate': 'exchange_rate',
            'fxrateupdatetimezone': 'fx_rate_update_timezone',
            'id': 'id',
            'includeinfxrateupdates': 'include_in_fx_rate_updates',
            'isbasecurrency': 'is_base_currency',
            'isinactive': 'is_inactive',
            'lastmodifieddate': 'last_modified_date',
            'name': 'name',
            'overridecurrencyformat': 'override_currency_format',
            'symbol': 'symbol',
            'symbolplacement': 'symbol_placement'
        }
        self.assertEqual(expected_rename_mapping_cols, actual_rename_mapping_cols, "columns should be mapped")

    def test_customer_columns_size(self):
        actual_rename_mapping_cols = self.rename_cols.get_mapped_columns("customer")
        self.assertEqual(56, len(actual_rename_mapping_cols), "Column size should match")

    def test_get_built_in_columns(self):
        expected_columns_string = "BUILTIN.DF( currencyprecision ) as currencyprecision,BUILTIN.DF( displaysymbol ) as displaysymbol," \
                                  "BUILTIN.DF( exchangerate ) as exchangerate,BUILTIN.DF( fxrateupdatetimezone ) as fxrateupdatetimezone," \
                                  "BUILTIN.DF( id ) as id,BUILTIN.DF( includeinfxrateupdates ) as includeinfxrateupdates," \
                                  "BUILTIN.DF( isbasecurrency ) as isbasecurrency,BUILTIN.DF( isinactive ) as isinactive," \
                                  "BUILTIN.DF( lastmodifieddate ) as lastmodifieddate,BUILTIN.DF( name ) as name," \
                                  "BUILTIN.DF( overridecurrencyformat ) as overridecurrencyformat,BUILTIN.DF( symbol ) as symbol," \
                                  "BUILTIN.DF( symbolplacement ) as symbolplacement"
        actual_rename_mapping_cols = self.rename_cols.get_built_in_columns("currency")
        self.assertEqual(expected_columns_string, actual_rename_mapping_cols, "Column string should match.")

    def test_dttypes(self):
        actual_rename_mapping_cols = self.rename_cols.get_dtypes_columns("invoice_data")
        self.assertEqual('string', actual_rename_mapping_cols['status'], 'Status type should be string')

    def test_zohocrm_dttypes(self):
        table_props = TableProps(source_name='zohocrm')
        dtypes_col_list = table_props.get_dtypes_columns(table_name='Accounts')
        print(dtypes_col_list)
        primary_keys = table_props.get_primary_keys(table_name='Accounts')
        print(primary_keys)

    def test_date(self):
        from datetime import datetime, timedelta
        start_date = self.rename_cols.get_start_date("invoice_data")
        end_date = self.rename_cols.get_end_date("invoice_data")
        #self.assertEqual('2022-01-01',start_date, 'Status type should be string')

        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        print(start_date)  # 👉️ 2023-09-24 00:00:00

        print('Start Date')
        print(start_date.strftime('%Y-%m-%d'))
        print('----------')
        while(start_date < end_date):
            delta_date = start_date + timedelta(days=7)
            print(delta_date.strftime('%Y-%m-%d'))
            start_date = delta_date

        print('End Date')
        end_date = delta_date + timedelta(days=1)
        print(end_date.strftime('%Y-%m-%d'))

    def test_file_name(self):
        from datetime import datetime

        now = datetime.now()
        load_type = 'il'
        file_format = 'json'
        file_date = now.strftime(
            "%Y-%m-%d-%H-%M-%S-%f")[:-3]  # [:-3] => Removing the 3 last characters as %f is for millis.
        file_name = f'{file_date}_utc_{load_type}.{file_format}'
        print(file_name)
        #self.assertEqual('2022-11-29-18-25-17-389_utc_il.json', file_name)

    def test_primary_keys(self):
        primary_keys = self.rename_cols.get_primary_keys("currency")
        self.assertEqual(['id'], primary_keys)




if __name__ == '__main__':
    unittest.main()

# rename $ with blank in every column name
# df.columns = df.columns.str.replace('$', '')
##rename specific column names
# df.rename(columns = {'team':'team_name', 'points':'points_scored'}, inplace = True)

# import re
# regex = r"[!\"#$%&'()*+,\-.\/:;<=>?@[\\\]^_`{|}~ ]+"
# X_trn.columns = X_trn.columns.str.replace(regex, '_', regex=True)
# X_tst.columns = X_tst.columns.str.replace(regex, '_', regex=True)