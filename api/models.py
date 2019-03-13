from django.db import models

# Create your models here.


class MessageToParticipant(models.Model):
    sub_heading = models.CharField(max_length=100, null=True, blank=True)
    bold_heading = models.CharField(max_length=100, null=True, blank=True)
    content = models.TextField(max_length=500, null=True, blank=True)
    issued_by = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.bold_heading) + " issued by " + str(self.issued_by)

