# -*- coding: utf-8 -*-

from flask import render_template, request, session, jsonify
from . import main
from .forms import RegisterFormContent
from flask_login import login_required, flash, current_user

from ..models import User
from .. import db

from ..const import MSGSEND_MINTIME, ErrNo, CODEVALID_MAXTIME
from ..helper import sendMesg, generate_verification_code, phoneCheck, passwordCheck
from datetime import datetime


@main.route('/')  # 首页
def index():
    return render_template('index.html')


@main.route('/register', methods={"POST", 'GET'})  # 注册
def register():
    parameters = request.values

    mobile = parameters.get("mobile")
    password = parameters.get("password", type=str, default=None)
    password_repeat = parameters.get("password_repeat", type=str, default=None)
    mobile_code = parameters.get("mobile_code", type=str, default=None)

    form = RegisterFormContent()
    form.mobile = mobile
    form.password = password
    form.password_repeat = password_repeat
    form.mobile_code = mobile_code

    result, msg = phoneCheck(mobile)
    if not result:
        flash(msg)
        return render_template('register.html', form=form)

    result, msg = passwordCheck(password)
    if not result:
        flash(msg)
        return render_template('register.html', form=form)

    # code = session["code"]
    code = "111111"

    if code != mobile_code:  # 验证码是否相等
        msg = "verification code wrong"
        flash(msg)
        return render_template('register.html', form=form)

    if "last_send_time" in session:  # 验证码有无过期
        last_send_time = session["last_send_time"]
    if last_send_time:
        last_send_time = datetime.strptime(last_send_time, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        if (current_time - last_send_time).seconds > CODEVALID_MAXTIME:
            msg = "verification code out of date"
            flash(msg)
            return render_template('register.html', form=form)

    if mobile:  # mobile 不为空
        user = User.query.filter(User.mobile == mobile).first()
        if user:  # 手机已被注册
            msg = "mobile already be registered"
            flash(msg)
            return render_template('register.html', form=form)
        else:
            msg = "register success, welcome"
            user = User()
            user.mobile = mobile
            user.password = password
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                msg = "register fail: "
                flash(msg + str(e))
                return render_template('register.html', form=form)
    else:
        msg = ErrNo.PARAM
        flash(msg)
        return render_template('register.html', form=form)
    return render_template('index.html')


@main.route('/get_verification_code', methods=["POST"])  # 验证手机号
def get_verification_code():
    success = False
    msg = ""

    mobile = request.args.get("mobile", type=str, default="")
    code = generate_verification_code()  # 随机产生6位验证码
    session["code"] = code

    last_send_time = None
    if "last_send_time" in session:
        last_send_time = session["last_send_time"]
    if last_send_time:
        last_send_time = datetime.strptime(last_send_time, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        if (current_time - last_send_time).seconds < MSGSEND_MINTIME:
            # no send
            msg = ErrNo.SMS
        else:
            sendMesg(mobile=mobile, code=str(code))
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session["last_send_time"] = current_time
            success = True
            msg = ErrNo.OK
    else:
        sendMesg(mobile=mobile, code=str(code))
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session["last_send_time"] = current_time
        success = True
        msg = ErrNo().OK

    return jsonify({
        "success": success,
        "msg": msg
    })


@main.route('/userInfo', methods={"POST"})  # 用户信息
@login_required
def userInfo():
    user = current_user._get_current_object()
    return jsonify({
        "userInfo": user.to_json()
    })


@main.route('/applay_status')  # 用户
@login_required
def user_apply_status():
    user = current_user._get_current_object()
    return jsonify({
        "apply_status": user.loan_app.apply_status
    })


@main.route('/userInfo/edit', methods={"POST"})  # 用户信息修改
@login_required
def userInfo_edit():
    return None


@main.route('/find/password', methods={"POST"})  # 用户密码找回
@login_required
def find_password():
    parameters = request.values

    mobile = parameters.get("mobile")


@main.route('/find/withdraw_password')  # 用户提现密码找回
@login_required
def find_withdraw_password():
    return None


@main.route('/loan_apply/info')  # 申请资料查看
@login_required
def loan_apply_info():
    return None


@main.route('/loan_apply/upload')  # 申请资料上传
@login_required
def loan_apply_upload():
    msg = ""
    user = current_user._get_current_object()
    if user.loan_app:
        flash(msg)
        return

    parameters = request.values

    apply_name = parameters.get("apply_name", type=str, default=None)
    gender = parameters.get("gender", type=int, default=None)
    marriage_status = parameters.get("marriage_status", type=str, default=None)
    bank_name = parameters.get("bank_name", type=str, default=None)
    bank_account = parameters.get("bank_name", type=str, default=None)
    company_address = parameters.get("company_address", type=str, default=None)
    company_mobile = parameters.get("company_mobile", type=str, default=None)
    urgent_contacter1 = parameters.get("urgent_contacter1", type=str, default=None)
    urgent_contacter2 = parameters.get("urgent_contacter2", type=str, default=None)

    image1 = parameters.get("image1", type=str, default=None)
    image2 = parameters.get("image2", type=str, default=None)
    image3 = parameters.get("image3", type=str, default=None)
    image4 = parameters.get("image4", type=str, default=None)


@main.route('/loan_amount')  # 申请状态额度
@login_required
def loan_apply_amount():
    user = current_user._get_current_object()
    return jsonify({
        "loan_amount": user.loan_app.loan_amount
    })


