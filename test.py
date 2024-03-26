import os
from typing import Tuple

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models

class Sample:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        """
        使用环境变量中的AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        access_key_id = "LTAI5t6d3mE8KWUbNc5rZqYY"
        access_key_secret = "Gw4XOONFrZBbfKF5PVpwh1HAtw288w"
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
        config.endpoint = 'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def send_verification_code(verification_code: str) -> bool:
        """
        发送验证码
        @param verification_code: 验证码
        @return: 是否发送成功
        """
        client = Sample.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='温室平台',
            template_code='SMS_464985173',
            phone_numbers='15212371894',  # TODO: Replace with the actual recipient's phone number
            template_param=f'{{"code":"{verification_code}"}}'
        )
        runtime = util_models.RuntimeOptions()
        try:
            response = client.send_sms_with_options(send_sms_request, runtime)
            # 这里简化处理，实际可能需要根据response的内容判断发送是否真正成功
            return True
        except Exception as e:
            print(e.message)
            return False

# 使用示例
if __name__ == '__main__':
    verification_code = '1234'  # 示例验证码
    success = Sample.send_verification_code(verification_code)
    print('发送成功' if success else '发送失败')
