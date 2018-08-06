from django.shortcuts import render

from .models import Result

from .data_processor import process_results


# Create your views here.
def index(request):

    killer_table, tails_table, begin, end = process_results()
    return render(request, 'killer/index.html', context={
        'killer': killer_table,
        'tails': tails_table,
        'begin_period': begin,
        'end_period': end
    })
