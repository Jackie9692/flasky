# -*- coding: utf-8 -*-

import random
from .const import ALLOWED_EXTENSIONS

def sendMesg(code=None, mobile=None, type=None):
    """ send message to the mobile

    :param code: the code to send to the mobile
    :param mobile: the mobile to send
    """
    print("send message: " + str(mobile))


def generate_verification_code():  # 只返回数字
    ''' 随机生成6位的验证码 '''
    code_list = []
    for i in range(10):  # 0-9数字
        code_list.append(str(i))
    # for i in range(65, 91): # A-Z
    # code_list.append(chr(i))
    # for i in range(97, 123): # a-z
    # code_list.append(chr(i))
    myslice = random.sample(code_list, 6)  # 从list中随机获取6个元素，作为一个片断返回
    verification_code = ''.join(myslice)  # list to string
    return verification_code


def phoneCheck(s):
    result = False
    msg = ""
    phoneprefix = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '150', '151', '152', '153',
                   '156', '158', '159', '170', '183', '182', '185', '186', '188', '189']

    if s:
        if len(s) != 11:
            msg = "check the mobile length"
        else:
            if s.isdigit():
                if s[:3] in phoneprefix:
                    msg = "The phone num is valid."
                    result = True
                else:
                    msg = "The phone num is invalid."
            else:
                msg = "mobile contain illegal character"
    else:
        pass

    return result, msg


def passwordCheck(s):
    result = False
    msg = ""

    if s:
        if len(s) < 6:
            msg = "password length is less than 6"
        else:
            result = True
    else:
        pass
    return result, msg

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS