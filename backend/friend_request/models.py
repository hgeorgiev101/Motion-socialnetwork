from django.db import models

from user.models import User


class FriendRequest(models.Model):
    status_choices = [
        (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Declined'),
    ]

    sent_date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sent_FR')
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='received_FR')
    status = models.IntegerField(choices=status_choices, default=1)

    def __str__(self):
        return f'Friend request ID:{self.id} from {self.sender} to {self.receiver}'
