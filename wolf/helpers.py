import os
import urllib

import zeep
from nanohttp import settings


class MaskanSmsProvider:
    def __init__(self):
        configuration = settings.maskan_web_service.sms
        self.sender_number = configuration.number
        self.username = configuration.username
        self.password = configuration.password
        self.company = configuration.company
        self.filename = urllib.parse.urljoin(
            'file:',
            urllib.request.pathname2url(
                configuration.filename
            )
        )

    def send(self, recipient_number, message_text):
        if recipient_number.startswith('98') \
                or recipient_number.startswith('+98'):
            recipient_number = f'0{recipient_number[2:]}'

        client = zeep.Client(self.filename)

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

