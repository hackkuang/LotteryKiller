from django.core.validators import MaxValueValidator
from django.db import models


# Create your models here.
class Result(models.Model):
    period = models.PositiveIntegerField()
    red1 = models.PositiveIntegerField(validators=[MaxValueValidator(33)])
    red2 = models.PositiveIntegerField(validators=[MaxValueValidator(33)])
    red3 = models.PositiveIntegerField(validators=[MaxValueValidator(33)])
    red4 = models.PositiveIntegerField(validators=[MaxValueValidator(33)])
    red5 = models.PositiveIntegerField(validators=[MaxValueValidator(33)])
    red6 = models.PositiveIntegerField(validators=[MaxValueValidator(33)])
    blue = models.PositiveIntegerField(validators=[MaxValueValidator(16)])

    class Meta:
        ordering = ('-period',)

    def __str__(self):
        args = [self.red1, self.red2, self.red3, self.red4, self.red5, self.red6, self.blue]
        desc = '{0}({1} )'.format(self.period, '{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}{:0>2d}'.format(*args))
        return desc


class Record(models.Model):
    time = models.DateTimeField(auto_now=True)
    begin_period = models.ForeignKey(Result, related_name='record_begin')
    end_period = models.ForeignKey(Result, related_name='record_end')

    class Meta:
        ordering = ('-time', )

    def __str__(self):
        return 'time: {0}; periods: {1} - {2}'.format(
            self.time.strftime("%Y-%m-%d %H:%M:%S"),
            int(self.begin_period.period),
            int(self.end_period.period)
        )
