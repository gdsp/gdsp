from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from tutor.models import Result
import cPickle as pickle
import sys, pdb, random, inspect, urllib

import tests
import modular_path as md


def test(request, test_name, level, FX):
    context = {}
    context['test_name'] = test_name
    context['level'] = level
    context['FX'] = FX

    test = tests.find(test_name, level, FX, request.user)
    correct = test.store_result(request) if request.method == 'POST' else False
    answer, fxs, sound, csd = test.check(request, correct) if request.method == 'POST' else test.first()

    context['choices'] = fxs
    context['answer'] = answer 
    context['sound'] = sound 
    context['csd'] = csd
    try:
        context['last_csd'] = Result.objects.filter(user = request.user).filter(correct = 1).latest('timestamp').csd
    except:
        context['last_csd'] = 'Not a single correct answer yet!?'
    context['msg'] = ''
    if request.method == 'POST':
        context['msg'] = 'Correct. Good job!' if correct else 'Oops, try again :)'
    config = {}
    execfile(md.systemfiles + '/effectsDict_edit.txt', config)
    context['effectsDict'] = config['effectsDict']
    return render_to_response('tutor/test.html', { 'context': context }, context_instance=RequestContext(request))

def results(request):
    context = {}
    context['results'] = Result.objects.aggregated_results(request.user)
    return render_to_response('tutor/results.html', { 'context': context }, context_instance=RequestContext(request))
