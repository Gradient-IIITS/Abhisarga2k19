import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.http import StreamingHttpResponse
from Event.models import Event, Team

from django.contrib.auth.decorators import login_required
from django.conf import settings

class Echo:
    """An object that implements just the write method of the file-like
    interface.
    """
    def write(self, value):
        """Write the value by returning it, instead of storing in a buffer."""
        return value

@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def some_streaming_csv_view(request):
    if request.user.is_superuser:
        if request.method == "GET":
            events = Event.objects.all()
            return render(request, "Other/csv_download.html", {"events": events})
        
        else:
            """A view that streams a large CSV file."""
            # Generate a sequence of rows. The range is based on the maximum number of
            # rows that can be handled by a single sheet in most spreadsheet
            # applications.
            event_id = request.POST.get('id')
            event = Event.objects.get(id=event_id)

            participants = Team.objects.filter(event__id=event.id)
            # print(participants)
            part_list = list()
            part_list.append([event.name, len(participants)])
            part_list.append([])

            if event.team_event:
                for participant in participants:
                    part_list.append([participant.team_name])
                    row = list()
                    row.append(participant.leader.first_name)
                    row.append(participant.leader.mobile_no)
                    row.append(participant.leader.college_name)
                    part_list.append(row)
                    row = list()
                    for member in participant.belong_to_team.all():
                        row.append(member.name)
                        row.append(member.mobile_no)
                    part_list.append(row)
                    part_list.append([])


                rows = (row for row in part_list)
                pseudo_buffer = Echo()
                writer = csv.writer(pseudo_buffer)
                response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                                 content_type="text/csv")
                response['Content-Disposition'] = 'attachment; filename="'+ str(event.name) +'-participant.csv"'
                return response
            else:
                for participant in participants:
                    row = list()
                    row.append(participant.leader.first_name)
                    row.append(participant.leader.mobile_no)
                    row.append(participant.leader.college_name)
                    part_list.append(row)
                    row = list()
                    for member in participant.belong_to_team.all():
                        row.append(member.name)
                        row.append(member.mobile_no)
                    part_list.append(row)
                    part_list.append([])


                rows = (row for row in part_list)
                pseudo_buffer = Echo()
                writer = csv.writer(pseudo_buffer)
                response = StreamingHttpResponse((writer.writerow(row) for row in rows),
                                                 content_type="text/csv")
                response['Content-Disposition'] = 'attachment; filename="'+ str(event.name) +'-participant.csv"'
                return response
