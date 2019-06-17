import os
import urllib

import suds


class MaskanSmsProvider:
    def __init__(self):
        self.sender_number = '10002501'
        self.username = 'otptest'
        self.password = 'testotp67'
        self.company = 'BANKMASKAN'
        self.url = 'http://1.2.4.164/MaskanSMSService.asmx?wsdl'
        self.wsdl_file_path = urllib.parse.urljoin(
            'file:',
            urllib.request.pathname2url(
                os.path.abspath('maskan_sms_soap')
            )
        )

    def send(self, recipient_number, message_text):
        if recipient_number.startswith('98') \
                or recipient_number.startswith('+98'):
            recipient_number = f'0{recipient_number[2:]}'

        client = suds.client.Client(self.wsdl_file_path, location=self.url)
        response = client.service.SendSMS_Single(
            strMessageText=message_text,
            strRecipientNumber=recipient_number,
            strSenderNumber=self.sender_number,
            strNumberUserName=self.username,
            strNumberPassword=self.password,
            strNumberCompany=self.company
        )

        if not response.SendSMS_SingleResult:
            raise MaskanSendSmsError(result_message=response.strResultMessage)

