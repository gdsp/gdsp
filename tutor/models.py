from django.db import models
from django.contrib.auth.models import User
import itertools
import pdb

class ResultManager(models.Manager):
    def aggregated_results(self, user):
        result = []
        for test in Result.objects.filter(user = user).values_list('test').distinct():
            q = Result.objects.filter(user = user).filter(test = test[0]).filter(cheated = False)
            correct = sum([ R.correct for R in q ])
            day_groups = []
            for key, group in itertools.groupby(q, key = lambda x: x.timestamp.date()):
                day_total = 0
                day_correct = 0
                for element in group:
                    day_total += 1
                    day_correct += element.correct
                day_groups.append((key, float(day_correct)/day_total * 100))
            result.append((test[0], correct, len(q), float(correct)/len(q) * 100 if q else 0, day_groups,
                           Result.objects.filter(user = user).filter(test = test[0]))) # Cheats included for display purposes.
        return result

class Result(models.Model):
    test = models.CharField(max_length = 256)
    correct = models.IntegerField()
    timestamp = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User)
    csd = models.CharField(max_length = 256)
    objects = ResultManager()
    cheated = models.BooleanField()

    def __unicode__(self):
        return 'Test ' + self.test + ' by ' + self.user.username + ' @ ' + str(self.timestamp) + ' Result: ' + str(self.correct)

class History(models.Model):
    user = models.ForeignKey(User)
    effect = models.CharField(max_length = 256)

    def __unicode__(self):
        return self.user.username + ': ' + self.effect
