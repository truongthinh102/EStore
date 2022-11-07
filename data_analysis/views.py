from django.shortcuts import render
from matplotlib.pyplot import boxplot
import pandas as pd
import os
from django.conf import settings
from data_analysis.utils import *

# Create your views here.
def series(request):
    views_1 = pd.Series([90006, 101141, 97297, 117182, 99637])
    views_1 = pd.DataFrame({'views': views_1})
    views_1 = views_1.to_html()

    views_2 = pd.Series([90006, 101141, 97297, 117182, 99637], ['a','b','c','d','e'])
    views_2 = pd.DataFrame({'views': views_2})
    views_2 = views_2.to_html()

    views_3 = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'data_analysis/data_views.csv'), squeeze=True)
    views_3 = pd.DataFrame({'views': views_3})
    # views_3 = views_3.to_html()
    views_3_head = views_3.head().to_html()
    views_3_tail = views_3.tail().to_html()

    return render(request, 'data_analysis/series.html', {
        'views_1': views_1,
        'views_2': views_2,
        'views_3_head': views_3_head,
        'views_3_tail': views_3_tail,
    })

def chart(request):
    # Histogram
    data_second = pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'data_analysis/dataset.xlsx'), sheet_name='Wait_times')
    hist = get_hist(data_second, 'seconds', 'Customer Wait Time')

    # Boxplot
    data_salaries = pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'data_analysis/salaries.xlsx'))
    boxplot = get_box(data_salaries, 'salary', 'Salary')

    # Bar Chart
    activity = pd.read_excel(os.path.join(settings.MEDIA_ROOT, 'data_analysis/dataset.xlsx'), sheet_name="Activity")
    barchart = get_bar(activity, 'Activity', 'Number_of_Students','After-School Activities')

    return render(request, 'data_analysis/chart.html', {
        'hist': hist,
        'boxplot': boxplot,
        'barchart': barchart,
    })