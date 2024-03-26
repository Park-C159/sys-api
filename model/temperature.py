# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import os
import sys

from typing import List

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient
import json


class Temperture:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> Dysmsapi20170525Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        
        access_key_id = "LTAI5t6d3mE8KWUbNc5rZqYY"
        access_key_secret = "Gw4XOONFrZBbfKF5PVpwh1HAtw288w"
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
        # Endpoint 请参考 https://api.aliyun.com/product/Dysmsapi
        config.endpoint = f'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)

    @staticmethod
    def send_temperature_warning(phone_number: str, temperature_num: float, offset_value: str):
        client = Temperture.create_client()
        sign_name = '温室预警'
        template_code = 'SMS_465387461'
        template_param = json.dumps({"code": temperature_num, "address": offset_value})

        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name=sign_name,
            template_code=template_code,
            phone_numbers=phone_number,
            template_param=template_param
        )

        runtime = util_models.RuntimeOptions()
        try:
            client.send_sms_with_options(send_sms_request, runtime)
            print("温度预警短信发送成功！")
        except Exception as error:
            print("温度预警短信发送失败：", error.message)

# if __name__ == '__main__':
#     # Temperture.main(sys.argv[1:])
#     Temperture.send_temperature_warning("15212371894", "12", "+1")
