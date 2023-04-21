from pydantic import BaseModel


class Preferences(BaseModel):
    event_type: str
    provider: str

    def __eq__(self, other: 'Preferences'):
        return self.event_type == other.event_type


if __name__ == '__main__':
    auth_email = Preferences(event_type='auth', provider='email')
    auth_email_2 = Preferences(event_type='auth', provider='email')
    auth_sms = Preferences(event_type='auth', provider='sms')
    auth_push = Preferences(event_type='auth', provider='push')
    my_list = [auth_email, auth_sms, auth_email]
    print(my_list.index(auth_push))
