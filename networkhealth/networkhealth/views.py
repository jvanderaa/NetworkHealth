from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
import pickle
import datetime
from command_output import get_command_output
from firewall_output import find_firewall_info
from ping_verify import determine_health, determine_health_all_sites
from . import forms

# pylint: disable=W0604, C0325


class TestPage(TemplateView):
    """ Test page template view """
    template_name = 'test.html'


class ThanksPage(TemplateView):
    """ Thanks page template view """
    template_name = 'thanks.html'


class HomePage(TemplateView):
    """ Home page template view """
    template_name = "index.html"

    # def get(self, request, *args, **kwargs):
    #     output = command_output()
    #     return super().get(request, *args, **kwargs)

def health(request):
    """ Function to check for device health. Individual site, not the whole
    environment.
    """
    form = forms.JustSiteListForm()
    output_dict = {'text': 'No site selected yet', 'form': form}
    if request.method == 'POST':
        form = forms.JustSiteListForm(request.POST)
        if form.is_valid():
            site = form.cleaned_data['site']
            if site != 'None':
                site_health, device_name, site = determine_health(site)
                output_dict = {
                    'text': site_health,
                    'form': form,
                    'site_name': site.upper(),
                    'datetime': datetime.datetime.now(),
                    'device_name': device_name
                }
            else:
                output_dict = {
                    'text': 'Please select a valid site.', 'form': form,
                }

    return render(request, 'health.html', output_dict)

def all_sites(request):
    """ Function to create the All Stations Health.
    1) Opens data.tmp file that is created by run_ping_check.py
    2) Sets the variable for the output to be passed to the django rendering
    engine
    3) render the web page including the dictionary.
    """
    # output = determine_health_all_sites()
    with open('data.tmp', 'rb') as pfile:
        start_time, maindata = pickle.load(pfile)
    output_dict = {
        'text': maindata,
        'datetime': start_time,
    }
    return render(request, 'networhealth/allremotes.html', output_dict)

def asa(request):
    """
    Function to provide ASA based commands.
    """
    form = forms.AsaFirewalls()
    output_dict = {
        'text': 'No device selected yet.',
        'form': form
    }
    
    if request.method == 'POST':
        form = forms.AsaFirewalls(request.POST)
        if form.is_valid():
            device_name = form.cleaned_data['device_name']
            command = form.cleaned_data['command_choice']
            output_dict = {
                'text': get_command_output(device_name=device_name, command=command),
                'form': form,
                'device_name': device_name,
                'datetime': datetime.datetime.now(),
                }
            # output_dict = {'text': "this is where a script would go."}
            return render(request, 'networkhealth/asa.html', output_dict)

    return render(request, 'networkhealth/asa.html', output_dict)


def firewalls(request):
    """
    Page to run commands against a device.
    """
    form = forms.SiteListArpForm()
    output_dict = {'text': 'No site selected yet.', 'form': form}
    if request.method == 'POST':
        form = forms.SiteListArpForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['site'],
                  form.cleaned_data['command_choice'])
            if form.cleaned_data['site'] != 'None':
                print('Gathering firewall info for %s' % form.cleaned_data['site'])
                output_dict = {
                    'text': find_firewall_info(site=form.cleaned_data['site'].upper()),
                    'form': form,
                    'site_name': form.cleaned_data['site'].upper(),
                    'datetime': datetime.datetime.now(),
                }
            else:
                output_dict = {
                    'text': 'Please select valid site.', 'form': form}
            return render(request, 'networkhealth/firewall.html', output_dict)

    return render(request, 'networkhealth/firewall.html', output_dict)


def routercommand(request):
    """ Page to get router commands """
    form = forms.RouterSiteListForm()
    output_dict = {'text': 'No device command selected yet.', 'form': form}
    if request.method == 'POST':
        form = forms.RouterSiteListForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['device_name'])
            output_dict = {
                'text': get_command_output(
                    device_name=form.cleaned_data['device_name'],
                    command=form.cleaned_data['command_choice']),
                'form': form
            }
            return render(request, 'networkhealth/routercommands.html', output_dict)

    return render(request, 'networkhealth/routercommands.html', output_dict)


def switchcommand(request):
    """ Page to run commands. Should move to being for switches only. """
    form = forms.SiteListForm()
    output_dict = {'text': 'No device command selected yet.', 'form': form}
    if request.method == 'POST':
        form = forms.SiteListForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['device_name'])
            output_dict = {
                'text': get_command_output(
                    device_name=form.cleaned_data['device_name'], 
                    command=form.cleaned_data['command_choice']),
                'form': form
            }
            # output_dict = {'text': "this is where a script would go."}
            return render(request, 'networkhealth/switchcommands.html', output_dict)

    return render(request, 'networkhealth/switchcommands.html', output_dict)


def index(request):
    """ Main index page. """

    return render(request, 'networkhealth/index.html')
