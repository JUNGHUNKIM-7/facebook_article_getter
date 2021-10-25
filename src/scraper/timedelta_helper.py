from datetime import timedelta
from dateutil.relativedelta import relativedelta
from typing import Union, Tuple


def make_month_date(time: str) -> Union[int, Tuple[int, int]]:
    parse_time = time.split(' ')
    if len(parse_time) == 1:
        extract_from_li = parse_time[0]
        if '어제' not in extract_from_li:
            time, chars = extract_from_li[0], extract_from_li[1:]
            if '시간' in chars:
                return 0
            else:
                return int(time)
        else:
            return 1
    elif len(parse_time) == 3:
        left_elem, right_elem = parse_time[0], parse_time[1]
        if len(parse_time[0]) == 2:
            if len(parse_time[1]) == 2:
                return int(left_elem[0]), int(right_elem[0])
            elif len(parse_time[1]) == 3:
                return int(left_elem[0]), int(right_elem[0:2])
            else:
                raise Exception('something went wrong')

        elif len(parse_time[0]) == 3:
            if len(parse_time[1]) == 2:
                return int(left_elem[0:2]), int(right_elem[0])
            elif len(parse_time[1]) == 3:
                return int(left_elem[0:2]), int(right_elem[0:2])
            else:
                raise Exception('something went wrong')
    else:
        raise Exception("data format is wrong")


def return_delta(data: str):
    if type(val := make_month_date(data)) is tuple:
        left, right = val[0], val[1]
        return relativedelta(months=left, days=right)
    else:
        return timedelta(days=val)
