from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import Mailing
from .services import send_mailing


def run_mailing(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)

    result = send_mailing(mailing)

    return HttpResponse(result)
