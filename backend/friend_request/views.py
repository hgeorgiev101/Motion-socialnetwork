import json
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView, GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from friend_request.models import FriendRequest, FriendList
from friend_request.permissions import GetPatchDeleteRequestPermission
from friend_request.serializers import FriendRequestSerializer, FriendListSerializer

User = get_user_model()

class SendRequest(ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response('GET not allowed', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        receiver = kwargs.get('receiver_id')
        if request.user.id == receiver:
            return Response("I'm sure you can find some friends, no need to be friends with yourself",
                            status=status.HTTP_400_BAD_REQUEST)
        friend_requests = self.get_queryset()
        friend_requests = friend_requests.filter(sender_id=request.user.id, receiver_id=receiver)
        if friend_requests:
            try:
                for fr in friend_requests:
                    if fr.status == 1:  # 1 is Pending
                        raise Exception('You have already sent them a friend request')
                    elif fr.status == 2:  # 2 is Accepted
                        raise Exception('You are already friends with this person')
                friend_request = FriendRequest(sender_id=request.user.id, receiver_id=receiver)
                friend_request.save()
                return Response( 'Friend Request sent!', status=status.HTTP_201_CREATED )
            except Exception as e:
                return Response(str(e), status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            friend_request = FriendRequest(sender_id=request.user.id, receiver_id=receiver)
            friend_request.save()
            return Response( 'Friend Request sent!', status=status.HTTP_201_CREATED )


class GetPatchDeleteRequest(GenericAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    lookup_url_kwarg = 'friend_request_id'
    permission_classes = [IsAuthenticated, GetPatchDeleteRequestPermission]

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer( instance, many=False )
        return Response( serializer.data )

    def patch(self, request, *args, **kwargs):
        queryset = self.get_object()
        if queryset.status != 1:
            return Response('Friend request does not have the status: Pending')
        body = request.data
        if body['action'] == 'accept':
            queryset.accept()
            serializer = self.get_serializer( queryset, many=False )
            return Response( serializer.data, status=status.HTTP_202_ACCEPTED )
        elif body['action'] == 'decline':
            queryset.decline()
            serializer = self.get_serializer( queryset, many=False )
            return Response( serializer.data, status=status.HTTP_202_ACCEPTED )
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        queryset = self.get_object()
        if queryset.status == 1:
            queryset.cancel()
            return Response('Friend request cancelled.', status=status.HTTP_200_OK)
        else:
            return Response( 'Cannot cancel a friend request that has been responded to',
                             status=status.HTTP_406_NOT_ACCEPTABLE )


class ListMyRequests(ListCreateAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(sender=request.user)
        serializer = self.get_serializer( queryset, many=True )
        return Response( serializer.data )


class ListIncomingRequests(ListCreateAPIView):
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(receiver=request.user, status=1)
        serializer = self.get_serializer( queryset, many=True )
        return Response( serializer.data )


class Unfriend(GenericAPIView):
    # queryset = FriendRequest.objects.all()
    serializer_class = FriendListSerializer
    lookup_url_kwarg = 'friend_id'
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response('GET not allowed', status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        friend_list = FriendList.objects.get(user=request.user)
        user_to_remove = User.objects.get(id=kwargs['friend_id'])
        request_to_delete = FriendRequest.objects.all()
        request_to_delete = request_to_delete.filter(
            Q(sender=request.user, receiver=user_to_remove) | Q(sender=user_to_remove, receiver=request.user)
        )
        friend_list.unfriend(user_to_remove)
        request_to_delete.delete()
        serializer = self.get_serializer( friend_list, many=False )
        return Response( serializer.data )
