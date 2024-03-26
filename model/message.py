import os
from typing import Tuple

from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_util import models as util_models
import json

class IdentifyCode:
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
    def send_verification_code(phone_number: str, verification_code: str) -> bool:
        """
        发送验证码
        @param verification_code: 验证码
        @return: 是否发送成功
        """
        client = IdentifyCode.create_client()
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='温室平台',
            template_code='SMS_464985173',
            phone_numbers=phone_number,  # TODO: Replace with the actual recipient's phone number
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

class Light:
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
    def send_light_warning(phone_number: str, light_num: float, offset_value: str):
        client = Light.create_client()
        template_param = f'{{"code": "{light_num}", "address": "{offset_value}"}}'
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='温室预警',
            template_code='SMS_465412412',
            phone_numbers=phone_number,
            template_param=template_param
        )
        runtime = util_models.RuntimeOptions()
        try:
            client.send_sms_with_options(send_sms_request, runtime)
            print(f"光照预警短信已发送至：{phone_number}")
        except Exception as error:
            print(f"发送光照预警短信失败: {error.message}")

class Humidity:
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
    def send_humidity_warning(phone_number: str, humidity_num: float, offset_value: str):
        client = Humidity.create_client()
        template_param = f'{{"code": "{humidity_num}", "address": "{offset_value}"}}'
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            sign_name='温室预警',
            template_code='SMS_465402395',
            phone_numbers=phone_number,
            template_param=template_param
        )
        runtime = util_models.RuntimeOptions()
        try:
            client.send_sms_with_options(send_sms_request, runtime)
            print(f"湿度预警短信已发送至：{phone_number}")
        except Exception as error:
            print(f"发送湿度预警短信失败: {error.message}")



    







