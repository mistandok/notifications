from pydantic import BaseModel, validator


class Preferences(BaseModel):
    event_type: str
    provider: str

    @validator('event_type', each_item=True)
    def check_event_type_name(cls, value):
        if value not in ('auth', 'email'):
            raise ValueError(f'Некорректное событие! поддерживаемые события: {("auth", "email")}')
        return value


if __name__ == '__main__':
    auth_email = Preferences(event_type='auth', provider='email')
    auth_email_2 = Preferences(event_type='auth', provider='email')
    auth_sms = Preferences(event_type='auth', provider='sms')
    auth_push = Preferences(event_type='auth', provider='push')
    my_list = [auth_email, auth_sms, auth_email]
    print(my_list.index(auth_push))
