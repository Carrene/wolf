import os
import urllib

import zeep
from nanohttp import settings


class MaskanSmsProvider:
    def __init__(self):
        self.sender_number = '10002501'
        self.username = 'otptest'
        self.password = 'testotp67'
        self.company = 'BANKMASKAN'
        self.filename = urllib.parse.urljoin(
            'file:',
            urllib.request.pathname2url(
                settings.maskan_web_service.sms.filename
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
            raise MaskanSendSmsError(result_message=response.strResultMessage)

