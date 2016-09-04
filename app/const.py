# -*- coding: utf-8 -*-

from enum import Enum
import os

UPLOAD_SIZE = 2 ** 24  # the maximum size of uploaded pictures
TOKEN_TIME_OUT_MIN = 1000000  # token lifetime
CODE_TIME_OUT_SEC = 300  # validation code lifetime
ADJOIN_BOOK_SPACE_SECONDS = 30 * 60  # protection space between two adjoin bookings
CARD_CHARGE_DURATION_SECONDS = 6 * 60 * 60  # maximum length of charging by owner card
ADMIN_USER = 'admin'  # admin login user name
ADMIN_PASS = 'admin123'  # admin login password

FLASKY_POSTS_PER_PAGE = 12  # page size


class BookStatus(Enum):
    NPAID = 0  # Guest Not Paid
    PAID = 1  # Guest Paid
    ACCEPT = 2  # Pile Owner Accept
    DECLINE = 3  # Pile Owner Decline
    CHARGING = 4  # Guest Start Charging
    COMPLETE = 5  # Guest Complete Charging
    OVERDUE = 6
    CANCEL = 7  # Guest cancel the book before charging


class ErrNo():
    OK = "success"  # Success
    PARAM = "Parameter invalid, lost, etc"  # Parameter invalid, lost, etc
    DB = "Database operation failure"
    DUP = "Duplicate key, i.e. user name used, mobile phone registered, etc"
    NOID = "No record, i.e. user, book not exists"
    INACT = "Inactive user"

    PASSWD = "Password incorrect"
    TOKEN = "Token incorrect"
    TIMEOUT = "Timeout"
    NOAUTH = "No authority"
    BIG = "Uploaded file exceeds the size limit"

    SMS = "Failed to send SMS"
    INVALID = "Invalid verification code"
    MNS = "Failed to send MNS message"


MSGSEND_MINTIME = 60  # minmal message send intervel time

CODEVALID_MAXTIME = 60 * 120  # max mobile code valid time

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static')
UPLOAD_FOLDER = os.path.join(UPLOAD_FOLDER, 'upload')  # 上传文件夹
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

ISOTIMEFORMAT = '%Y%m%d%H%M%S'  # 图片命名
ADMIN_USERNAME = "Admin"