import json
import pickle
import random


def random_key(length:int):
    """
    生成随机数字，密码
    :param length:
    :return:
    """
    ran_key = ''
    for i in range(length): ran_key += str(random.randint(0,9))
    return ran_key


def encrypt(raw:str, key_str=None):
    """
    加密
    :param raw:
    :param key_str:
    :return:
    """
    if not isinstance(raw, str): raise TypeError('raw required str but got {}'.format(type(raw).__name__))
    raw_bytes = raw.encode()
    raw_int = int.from_bytes(raw_bytes, 'big')
    if not key_str: key_str = random_key(10)
    key_int = int.from_bytes(key_str.encode(), 'big')
    data = raw_int ^ key_int
    return data, key_str


def decrypt(encrypted:int, key:str):
    """
    解密
    :param encrypted:
    :param key:
    :return:
    """
    if not isinstance(encrypted, int): raise TypeError('encrypted required int but got {}'.format(type(encrypted).__name__))
    key_int:int = int.from_bytes(key.encode(),'big')
    decrypted:int = encrypted ^ key_int
    length:int = (decrypted.bit_length() + 7 )// 8
    decrypted_bytes:bytes = int.to_bytes(decrypted, length, byteorder='big')
    return decrypted_bytes.decode()



def encryptFile(path:str,outpath:str, key:str):
    with open(path, 'rb') as f:
        newkey = int.from_bytes(bytes(key, 'utf-8'), 'big')
        newkey = newkey * newkey
        data = b'file' + f.read(1000) + bytes(str(newkey),'utf-8') + f.read()
        with open(outpath, 'wb') as f2:
            new_data = {'file':data}
            pickle.dump(new_data,f2)


def decryptFile(path:str, key:str):
    with open(path, 'rb') as f:
        raw = pickle.loads(f.read())
        for k, v in raw.items():
            newkey = int.from_bytes(bytes(key, 'utf-8'), 'big')
            newkey = newkey * newkey
            length = len(str(newkey))

            data = v[4:1004] + v[1004+length:]
            return data


if __name__ == '__main__':
    # encryptFile(r"E:\Programme\GIT\Python\Hotchpotch\ToolBox\Ico\audit.png",'./file.png','bnm123')
    d = decryptFile('file.png','bnm123')
    with open('./file2.png','wb') as f:
        f.write(d)


