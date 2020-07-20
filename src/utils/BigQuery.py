from google.cloud import bigquery


class BigQuery:

    # Initialize test data for big query
    def __init__(self, test_data):
        self.test_data_dict = {}
        self.construct_test_data(test_data)

    # Get value and param condition from test data file
    def construct_test_data(self, test_data):
        for k, v in test_data.items():
            for qry_param_nm in v['QueryParamNm']:
                self.test_data_dict[qry_param_nm] = {'Values': v['Values'], 'ParamCond': v['ParamCond']}

    # Execute query and return results in dictionary
    def get_query_result(self, query):
        exp_dict = self.execute_query(self.construct_query(query))
        return exp_dict

    def execute_query(self, query):
        headers = []
        list_output = []
        client = bigquery.Client() # Construct a BigQuery client object.
        query_job = client.query(query)  # Make an API request.
        for row in query_job:
            if len(headers) == 0:
                headers = [f for f in row.keys()]
            result = {}
            if len(headers) > 1:
                for header in headers:
                    result[header.lower()] = str(row[header]) if str(row[header]) != 'None' else '0'
            else:
                header = headers[0]
                result[header.lower()] = str(row[header]) if str(row[header]) != 'None' else '0'
            list_output.append(result)
        return list_output

    # Construct a query with where conditions
    def construct_query(self, query):
        test_data = self.test_data_dict
        qry_cols = test_data.keys()
        cond_lst = [self.construct_query_condition(qry_cols, test_data)]
        return query.format(*cond_lst)

    def construct_query_condition(self, qry_cols, test_data):
        mul_cond = ''
        for qry_col_nm in qry_cols:
            if qry_col_nm in test_data:
                values = test_data.get(qry_col_nm)['Values']
                if 'all' not in values and '' != values[0].strip():
                    param_cond = test_data.get(qry_col_nm)['ParamCond']
                    if param_cond == 'in':
                        cond = qry_col_nm + " in('" + "','".join(values).strip() + "')"
                    elif param_cond == 'between':
                        cond = qry_col_nm + ' between ' + values[0].replace('-', '') + ' and ' + values[1].replace('-',
                                                                                                                   '')
                    else:
                        cond = qry_col_nm + " " + param_cond + values[0]
                    mul_cond += " and " + cond if mul_cond != '' else cond
        return mul_cond
