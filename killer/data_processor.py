import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LotteryKiller.settings')
django.setup()

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import numpy as np
import pandas as pd

from django.forms.models import model_to_dict

from killer.models import Result

from collections import Counter

def judge_sum_in(arrLike):
    result = arrLike[7] in list(arrLike[:6])
    return result


def way1(killnum_data):
    # 1
    r1r2sum = (killnum_data['red1'] + killnum_data['red2']).shift(periods=1, axis=0)
    killnum_data1 = killnum_data.copy()
    killnum_data1['r1r2sum'] = r1r2sum
    killnum_data1['way1result'] = killnum_data1.apply(judge_sum_in, axis=1)
    return killnum_data1[['r1r2sum', 'way1result']]


def way2(killnum_data):
    killnum_data2 = killnum_data.copy()

    l = list(killnum_data.iloc[:, 0])
    length = len(l)
    p1p2sum = [np.NaN, np.NaN]
    for i, elem in enumerate(l):
        if (i + 2) < length:
            p1p2sum.append(elem + l[i + 1])
    killnum_data2['p1p2sum'] = p1p2sum
    killnum_data2['way2result'] = killnum_data2.apply(judge_sum_in, axis=1)

    return killnum_data2[['p1p2sum', 'way2result']]


# 3
def way3(killnum_data):
    killnum_data3 = killnum_data.copy()

    l = list(killnum_data.iloc[:, 1])
    length = len(l)
    p1p2sum_red2 = [np.NaN, np.NaN]
    for i, elem in enumerate(l):
        if (i + 2) < length:
            p1p2sum_red2.append(elem + l[i + 1])
    killnum_data3['p1p2sum_red2'] = p1p2sum_red2
    killnum_data3['way3result'] = killnum_data3.apply(judge_sum_in, axis=1)

    return killnum_data3[['p1p2sum_red2', 'way3result']]


# 4
def way4(killnum_data):
    killnum_data4 = killnum_data.copy()

    l = list(killnum_data.iloc[:, 6])
    length = len(l)
    p1p2sum_blue = [np.NaN, np.NaN]
    for i, elem in enumerate(l):
        if (i + 2) < length:
            p1p2sum_blue.append(elem + l[i + 1])
    killnum_data4['p1p2sum_blue'] = p1p2sum_blue
    killnum_data4['way4result'] = killnum_data4.apply(judge_sum_in, axis=1)

    return killnum_data4[['p1p2sum_blue', 'way4result']]


def get_digits(x):
    return x % 10


def map2times(arrLike):
    c = Counter(arrLike)
    target = range(0, 10)
    result = []
    for i in target:
        result.append(c[i])
    return result


def process_tail(killnum_data):
    tails = killnum_data.copy()
    tail_num = tails.iloc[:, :6].apply(get_digits)
    tail_exist = pd.DataFrame(tail_num.apply(map2times, axis=1).to_dict()).T
    tail_exist = tail_exist.reindex(index=killnum_data.index)
    tail_exist = tail_exist.reset_index()
    return tail_exist


def process_results():
    model_list = [model_to_dict(model) for model in Result.objects.all()[0:32]]
    model_list = model_list[::-1]
    begin = model_list[0]['period']
    end = model_list[-1]['period']
    killnum_data = pd.DataFrame(model_list, index=list(range(0, 32)))
    killnum_data = killnum_data.set_index('period').drop('id', axis='columns')
    killnum_data = killnum_data.reindex(
        columns=['red1', 'red2', 'red3', 'red4', 'red5', 'red6', 'blue']
    )

    processed = pd.concat([killnum_data, way1(killnum_data), way2(killnum_data), way3(killnum_data), way4(killnum_data)], axis=1)
    processed = processed.reset_index().iloc[2:, :]
    # print(process_tail(killnum_data).values)
    return processed.values, process_tail(killnum_data).values, begin, end


if __name__ == '__main__':
    process_results()
