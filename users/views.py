from rest_framework.views import APIView
from rest_framework.response import Response
import json

class ReadWrite:
    file_name = None

    @classmethod
    def load_users(cls):
        try:
            with open(cls.file_name, 'r') as file:
                return json.load(file)
        except (Exception, ) as err:
            print(err)

    @classmethod
    def add_user(cls, user):
        try:
            with open(cls.file_name, 'w') as file:
                json.dump(user, file)
        except (Exception,) as err:
            print(err)

class MyAPIView(APIView, ReadWrite):
    file_name = 'users.json'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.users = self.load_users()


class UserListCreateView(MyAPIView):

    def get(self, *args, **kwargs):
        return Response(self.users)

    def post(self, *args, **kwargs):
        user = self.request.data
        user['id'] = self.users[-1]['id']+1 if self.users else 1
        self.users.append(user)
        self.add_user(self.users)
        return Response(user)


class UserRetrieveUpdateDestroyView(MyAPIView):
    def get(self, *args, **kwargs):
        pk = kwargs.get('pk')
        user = [i for i in self.users if i['id'] is pk]
        if not user:
            return Response('Not Found')
        else:
            return Response(user)

    def put(self, *args, **kwargs):
        new_user = self.request.data
        pk = kwargs.get('pk')
        index = None
        for i in range(len(self.users)):
            if self.users[i]['id'] is pk:
                index = i
                break
        if index:
            self.users[index]['name'] = new_user['name']
            self.users[index]['age'] = new_user['age']
            self.add_user(self.users)
        else:
            return Response('Not Found')
        return Response(self.users[index])

    def delete(self, *args, **kwargs):
        pk = kwargs.get('pk')
        index = None
        for i in range(len(self.users)):
            if self.users[i]['id'] is pk:
                index = i
                break

        if index:
            del self.users[index]
            self.add_user(self.users)
        else:
            return Response('Not Found')

        return Response('deleted')

