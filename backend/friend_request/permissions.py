from rest_framework.permissions import BasePermission


class GetPatchDeleteRequestPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        print(request.method)
        if request.method == 'GET':
            if request.user == obj.sender or request.user == obj.receiver:
                print('this is in the get')
                return True
        if request.method == 'PATCH' and request.user == obj.receiver:
            return True
        if request.method == 'DELETE' and request.user == obj.sender:
            return True
        return False
