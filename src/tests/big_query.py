from collections import defaultdict
from google.cloud import bigquery
from src.utils.json_parser import JsonParser
from src.utils.utilities import Utilities
import os

class BigQuery:

    @staticmethod
    def query_result(dashboard, widget, col_nm):
        # widget wise query
        widget = widget.replace('.json', '')
        queries = Utilities.read_file("queries", dashboard, widget, ".txt")
        cols = queries[len(queries) - 1].split(',')
        queries.pop()
        for query in queries:
            formatted_query = BigQuery.construct_query(query, cols)
            result = BigQuery.client(formatted_query, col_nm)
        return result

    @staticmethod
    def client(query, col_nm):
        # Construct a BigQuery client object.
        my_dict = defaultdict(list)
        try:
            client = bigquery.Client()
            query_job = client.query(query)  # Make an API request.
            for row in query_job:
                # Row values can be accessed by field name or index.
                for col in col_nm:
                    if '!' not in col:
                        data = Utilities.round_off(str(row[col.replace('*', '')]))
                        my_dict[col].append(data)
        except BaseException:
            for col in col_nm:
                my_dict[col].append(0) if '!' not in col else ''
        return my_dict

    @staticmethod
    def construct_query(query, cols):
        # Construct a query with the required conditions
        mul_cond = ''
        #get the column names which needs to be a part of the query
        my_dict = JsonParser.column_name_mapping()
        for col_nm in cols:
            if 'calendar' in col_nm:
                if "all" != os.getenv('from_date').strip().lower() and os.getenv('from_date').strip() != '' \
                        if os.getenv('from_date') is not None else False:
                    mul_cond = col_nm + " between " + os.getenv('from_date').replace("-", "") + " and " + os.getenv(
                        'to_date').replace("-", "") + " "
            elif "all" != os.getenv(col_nm).strip().lower() and os.getenv(col_nm).strip() != '' \
                    if os.getenv(col_nm) is not None else False:
                values = os.getenv(col_nm).strip().split(',')
                lst_val = []
                for j in range(0, len(values)):
                    lst_val.append(values[j])
                cond = col_nm + " in (" + str(lst_val).replace("[", "").replace("]", "") + ")"
                mul_cond += " and " + cond if mul_cond != '' else cond
        return query.format(mul_cond)
