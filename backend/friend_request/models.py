from django.db import models

from project import settings
from user.models import User


class FriendRequest(models.Model):
    status_choices = [
        (1, 'Pending'),
        (2, 'Accepted'),
        (3, 'Declined'),
        (4, 'Cancelled'),
    ]

    sent_date = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_FR')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_FR')
    status = models.IntegerField(choices=status_choices, default=1)

    def __str__(self):
        return f'Friend request ID:{self.id} from {self.sender.username} to {self.receiver.username}'

    def accept(self):
        sender_FR = FriendList.objects.get_or_create(user=self.sender)
        sender_FR[0].add_friend(self.receiver)
        reciever_FR = FriendList.objects.get_or_create(user=self.receiver)
        reciever_FR[0].add_friend(self.sender)
        self.status = 2
        self.save()

    def decline(self):
        self.status = 3
        self.save()

    def cancel(self):
        self.status = 4
        self.save()


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user')

    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='friends')

    def __str__(self):
        return f"{self.user.username} : {self.user.first_name} {self.user.last_name}"

    def add_friend(self, account):
        if account not in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removed_user):  # self is the remover / initiator
        self.remove_friend(removed_user)

        # removing the remover from the others list
        removed_user_FL = FriendList.objects.get(user=removed_user)
        removed_user_FL.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False
