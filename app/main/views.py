# -*- coding: utf-8 -*-

from flask import render_template, request, session, jsonify, redirect
from . import main
from .forms import RegisterFormContent
from flask_login import login_required, flash, current_user

from ..models import User, Loan_application
from .. import db

from ..const import MSGSEND_MINTIME, ErrNo, CODEVALID_MAXTIME, UPLOAD_FOLDER, ISOTIMEFORMAT
from ..helper import sendMesg, generate_verification_code, phoneCheck, passwordCheck, allowed_file
from datetime import datetime
import time

import os


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


@main.route('/loan_apply/upload', methods={"POST", "GET"})  # 申请资料上传
@login_required
def loan_apply_upload():
    if request.method == 'GET':
        return render_template("applyLoan.html")
    else:
        msg = ""
        success = False

        user = current_user._get_current_object()
        loan_app = Loan_application.query.filter(Loan_application.mobile == user.mobile).first()
        if loan_app:
            msg = "已提交申请，审核中"
            return jsonify({
                "success": success,
                "msg": msg
            })

        parameters = request.values
        images = request.files

        if len(parameters) < 9 or len(images) < 4:  # 参数必须全部含有
            msg = ErrNo.PARAM
            return jsonify({
                "success": success,
                "msg": msg
            })

        apply_name = parameters.get("apply_name", type=str, default=None)
        gender = parameters.get("gender", type=int, default=None)
        marriage_status = parameters.get("marriage_status", type=str, default=None)
        bank_name = parameters.get("bank_name", type=str, default=None)
        bank_account = parameters.get("bank_account", type=str, default=None)
        company_address = parameters.get("company_address", type=str, default=None)
        company_mobile = parameters.get("company_mobile", type=str, default=None)
        urgent_contacter1 = parameters.get("urgent_contacter1", type=str, default=None)
        urgent_contacter2 = parameters.get("urgent_contacter2", type=str, default=None)

        image1 = images.get("image1", default=None)
        image2 = images.get("image2", default=None)
        image3 = images.get("image3", default=None)
        image4 = images.get("image4", default=None)

        loan = Loan_application()
        loan.apply_name = apply_name
        loan.gender = gender
        loan.marriage_status = marriage_status
        loan.bank_name = bank_name
        loan.bank_account = bank_account
        loan.company_address = company_address
        loan.company_mobile = company_mobile
        loan.urgent_contacter1 = urgent_contacter1
        loan.urgent_contacter2 = urgent_contacter2
        loan.apply_status = 0

        if image1 and allowed_file(image1.filename):
            suffix = "." + image1.filename.rsplit('.', 1)[1]
            filename = str(time.strftime(ISOTIMEFORMAT)) + str(generate_verification_code()) + str(suffix)
            image1.save(os.path.join(UPLOAD_FOLDER, filename))
            loan.image1 = filename

        if image2 and allowed_file(image2.filename):
            suffix = "." + image1.filename.rsplit('.', 1)[1]
            filename = str(time.strftime(ISOTIMEFORMAT)) + str(generate_verification_code()) + str(suffix)
            image2.save(os.path.join(UPLOAD_FOLDER, filename))
            loan.image2 = filename

        if image3 and allowed_file(image3.filename):
            suffix = "." + image1.filename.rsplit('.', 1)[1]
            filename = str(time.strftime(ISOTIMEFORMAT)) + str(generate_verification_code()) + str(suffix)
            image3.save(os.path.join(UPLOAD_FOLDER, filename))
            loan.image3 = filename

        if image4 and allowed_file(image4.filename):
            suffix = "." + image1.filename.rsplit('.', 1)[1]
            filename = str(time.strftime(ISOTIMEFORMAT)) + str(generate_verification_code()) + str(suffix)
            image4.save(os.path.join(UPLOAD_FOLDER, filename))
            loan.image4 = filename

        user = current_user._get_current_object()
        mobile = user.mobile
        loan.mobile = mobile

        try:
            db.session.add(loan)
            db.session.commit()
            success = True
            msg = "申请成功，敬请期待"
        except Exception as e:
            msg = msg + str(e)
            return jsonify({
                "success": success,
                "msg": msg
            })

        return jsonify({
            "success": success,
            "msg": msg
        })


@main.route('/loan_amount')  # 申请状态额度
@login_required
def loan_apply_amount():
    user = current_user._get_current_object()
    return jsonify({
        "loan_amount": user.loan_app.loan_amount
    })

