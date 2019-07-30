from django.shortcuts import render
from .models import *
import datetime
from django.db.models import Sum
import matplotlib.pyplot as plt
import math, random
import PIL.Image as Image
from django.http import HttpResponse

def UsageView(request,time_len = 15,time_peroid = 'minutes'):
    filter = {}
    filter[time_peroid] = time_len
    logs = AppUsageLog.objects.filter(
        ts__gte = datetime.datetime.now() - datetime.timedelta(**filter)
    ).values('app').annotate(
        txs=Sum('rx'),
        rxs=Sum('tx')
    ).order_by('-rxs')
    return render(request,'UsageView.html',{'logs':logs,'time_peroid':time_peroid,'time_len':time_len})

def AppView(request,app,time_len = 15,time_peroid = 'minutes'):
    return render(request,'AppView.html',{'time_peroid':time_peroid,'time_len':time_len,'app':app})

def AppUsageImage(request,app,time_len = 15,time_peroid = 'minutes'):
    filter = {}
    filter[time_peroid] = time_len
    logs = AppUsageLog.objects.filter(
        ts__gte = datetime.datetime.now() - datetime.timedelta(**filter),
        app = app
    ).order_by('ts')

    fig = plt.figure(figsize=(20,10))
    ax = fig.add_subplot(111)
    ax.set_ylabel('bytes')
    x = [ log.ts for log in logs]
    plt.plot(x,[ log.tx for log in logs],'r.-',label='TX')
    plt.plot(x,[ log.rx for log in logs],'b.-',label='RX')
    plt.legend()
    fig.tight_layout()

    buffer = HttpResponse()
    buffer['Content-Type'] = 'image/png'
    canvas = fig.canvas
    canvas.draw()
    pilImage = Image.frombytes("RGB", canvas.get_width_height(), canvas.tostring_rgb())
    pilImage.save(buffer, "PNG")

    return buffer
