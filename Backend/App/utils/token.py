# @Author: LiXiang
# @Time: 2023/11/5 9:01
# @version: 1.0
import jwt
import time

secret_key = 'Great_Librarian'  # token密钥
# token_time = 60 * 60 * 24 * 3  # 设置令牌时间
# token_time = 30  # 设置令牌时间
algorithm = 'HS256'


# 创建JWT
def encode(user_id, token_time):
    print('正在生成token*********')
    # 生成字典，包含具体信息
    payload = {
        # 公共声明
        'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
        'exp': time.time() + token_time,  # (Expiration Time) 此token的过期时间的时间戳
        # 'iss': 'Issuer',  # (Issuer) 指明此token的签发者
        # 私有声明
        'data': {
            'id': user_id,
            'timeEnd': time.time() + token_time
        }
    }
    return jwt.encode(payload, secret_key, algorithm)


# 解码和验证 JWT
def decode(token):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
        # print(f"token解码信息的id:{decoded['data']['id']}")
        return True, decoded['data']['id']
    except Exception as e:
        # print(f'token过期-----{e}')
        return False

# code = encode('123456', 30)
# time.sleep(1)
# decode(code)
