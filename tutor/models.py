import datetime
from collections import namedtuple

from django.db import models
from django.contrib.auth.models import User
import itertools
import pdb

class ResultManager(models.Manager):
    def aggregated_results(self, user, lesson_id = False):

        timedelta = namedtuple('TimeDelta', 'hours minutes seconds total_seconds')

        result = []
        if lesson_id:
            tests = Result.objects.filter(user = user).filter(lesson = lesson_id).values_list('test').distinct()
        else:
            tests = Result.objects.filter(user = user).values_list('test').distinct()

        time_threshold = datetime.timedelta(0,60) # 10 minute exclusion from time calculation - for this case, we assume the student left the computer.

        for test in tests:
            if lesson_id:
                q = Result.objects.filter(user = user).filter(lesson = lesson_id).filter(test = test[0]).filter(cheated = False)
            else:
                q = Result.objects.filter(user = user).filter(test = test[0]).filter(cheated = False)
            correct = sum([ R.correct for R in q ])
            day_groups = []
            time_spent = datetime.timedelta(0,0)

            for key, group in itertools.groupby(q, key = lambda x: x.timestamp.date()):
                day_total = 0
                day_correct = 0

                previous_date = False                
                for element in group:
                    day_total += 1
                    day_correct += element.correct
                    if not previous_date:
                        previous_date = element.timestamp
                    
                    if element.timestamp - previous_date < time_threshold:
                        time_spent += element.timestamp - previous_date
                        
                    print element.timestamp, element.timestamp - previous_date, element.timestamp - previous_date > time_threshold, time_spent
                    previous_date = element.timestamp

                day_groups.append((key, float(day_correct)/day_total * 100))

            s = time_spent.total_seconds()
            hours, remainder = divmod(s, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_spent = timedelta(int(hours), int(minutes), int(seconds), int(s))
                
            result.append((test[0], correct, len(q), float(correct)/len(q) * 100 if q else 0, day_groups,
                           Result.objects.filter(user = user).filter(lesson = lesson_id).filter(test = test[0]) if lesson_id else Result.objects.filter(user = user).filter(test = test[0]),
                           time_spent)) # Cheats included for display purposes.
        return result

class Result(models.Model):
    lesson = models.CharField(max_length = 256, default='dummy') # This is the Lesson primary key.
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
