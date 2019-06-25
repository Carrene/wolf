import urllib

import zeep
from nanohttp import settings

from wolf.exceptions import MaskanSendSmsError


def create_soap_client(wsdl):
    return zeep.Client(wsdl)


class MaskanSmsProvider:
    def __init__(self):
        configuration = settings.maskan_web_service.sms
        self.sender_number = configuration.number
        self.username = configuration.username
        self.password = configuration.password
        self.company = configuration.company
        self.wsdl = configuration.url

    def send(self, recipient_number, message_text, sms_service_url=None):
        if recipient_number.startswith('98') \
                or recipient_number.startswith('+98'):
            recipient_number = f'0{recipient_number[2:]}'

        client = create_soap_client(self.wsdl)

        if sms_service_url:
            client.wsdl.services['MaskanSendService'] \
            .ports['MaskanSendServiceSoap'] \
            .binding_options['address'] = sms_service_url

        response = client.service.SendSMS_Single(
            strMessageText=message_text,
            strRecipientNumber=recipient_number,
            strSenderNumber=self.sender_number,
            strNumberUsername=self.username,
            strNumberPassword=self.password,
            strNumberCompany=self.company
        )

        if not response.SendSMS_SingleResult:
            raise MaskanSendSmsError()

