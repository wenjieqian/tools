def getWebhook(hook,secret):
    '''
    @Desc   : 基于时间戳和钉钉机器人密钥计算签名，并拼接到Webhook URL
    @Author : Wenjie Qian
    @Email  : wenjieqian@foxmail.com
    @Param  :
        hook : str 钉钉机器人原始Webhook
        secret : str 钉钉机器人密钥
    @Return :
        Webhook : str 加签后的Webhook
    '''
    import time
    import hmac
    import hashlib
    import base64
    try:
        from urllib.parse import quote_plus # py3
    except ImportError:
        from urllib import quote_plus # py2
    timestamp = round(time.time() * 1000)
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = quote_plus(base64.b64encode(hmac_code)) 
    Webhook = hook + '&timestamp=%s&sign=%s'%(timestamp,sign)
    return Webhook
    


if __name__ == "__main__":
    hook = 'https://oapi.dingtalk.com/robot/send?access_token=d5a9886452ac194cbbe22a29638a81117f02ae7c9b11e6d95b1a038f6f3eXXXX'
    secret = 'SEC003a9af8324869e78b9b8f5297810654f3b5d92f0fde85afed91b7dbbccbxxxx'
    Webhook = getWebhook(hook,secret)
    print(Webhook)
