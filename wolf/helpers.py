import urllib

import zeep
from nanohttp import settings

from wolf.exceptions import MaskanSendSmsError


def create_soap_client(wsdl):
    return zeep.Client(wsdl)


class MaskanSmsProvider:
    def __init__(self):
        self.configuration = settings.maskan_web_service.sms
        self.sender_number = self.configuration.number
        self.username = self.configuration.username
        self.password = self.configuration.password
        self.company = self.configuration.company
        self.wsdl_url = self.configuration.wsdl_url

    def send(self, recipient_number, message_text):
        if recipient_number.startswith('98') \
                or recipient_number.startswith('+98'):
            recipient_number = f'0{recipient_number[2:]}'

        client = create_soap_client(self.wsdl_url)

        if hasattr(self.configuration, 'test_url'):
            client.wsdl.services['MaskanSendService'] \
            .ports['MaskanSendServiceSoap'] \
            .binding_options['address'] = self.configuration.test_url

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

