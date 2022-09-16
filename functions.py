from datetime import datetime


def get_unique_sorts(df, column_name):
    sorts = []
    for index, row in enumerate(df.iterrows()):
            # print(row[1]['Contains'])
            sort = row[1][column_name]
            if sort not in sorts:
                sorts.append(sort)
                
    return list(set(sorts))


def get_sorts_in_dict(unique_sorts, df, needle_column_name, haystack_column_name):
    bat_dict = {}

    for key in unique_sorts:
        bat_dict[key] = []
        temp_df = df.loc[df[needle_column_name] == key]
        temp_list = temp_df[haystack_column_name].tolist()
        bat_dict[key] = temp_list
    
    return bat_dict

def prepare_dict_for_df(_dict):
    longest_column = 0
    for key, values in _dict.items():
        if len(values) > longest_column:
            longest_column = len(values)
        
    for key, values in _dict.items():
        if len(values) < longest_column:
            diff = longest_column - len(values)
            for i in range(diff):
                _dict[key].append("")
    
    return _dict

def get_date_str(date_format):
    dt = datetime.now()
    ts = datetime.timestamp(dt)
    date_time = datetime.fromtimestamp(ts)
    return date_time.strftime(date_format)