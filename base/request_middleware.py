# -*- coding: utf-8 -*-
"""
Django middleware of request for logs
"""
from __future__ import unicode_literals

import json
import logging
import threading

from django.utils.deprecation import MiddlewareMixin

local = threading.local()
logger = logging.getLogger('tracer')


class RequestIDFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(local, 'request_id', "none")
        return True


def get_current_time(format=None):
    """
    获取当前时间
    :param format: 时间格式
    :return:
    """
    from datetime import datetime
    dt = datetime.now()
    if format:
        result = dt.strftime(format)
    else:
        result = dt.strftime("%Y/%m/%d %H:%M:%S")
    return result


def base_n(num, b):
    """
    将数字num转换为b进制
    :param num:
    :param b:
    :return:
    """
    return ((num == 0) and "0") or \
           (base_n(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def generate_sid():
    """
    生成sid
    :return:
    """
    sid = get_current_time("%H%M%S%f")
    sid = int(sid)
    # 将 10 进制转为 32 进制
    sid = base_n(sid, 32)
    # 反转
    return "{}".format(sid)[::-1]


class RequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        """
        绑定请求id
        :param request:
        """
        local.request_id = request.META.get('HTTP_X_REQUEST_ID', generate_sid())

    def process_response(self, request, response):
        """
        格式化日志
        :param request:
        :param response:
        :return:
        """
        log_list = ['\n']
        log_list.append('======================Request Start======================')
        log_list.append('TraceId: {}'.format(local.request_id))
        log_list.append('Request: {}, {}, {}'.format(request.path, request.method, response.status_code))

        if request.method == 'GET':
            log_list.append("Input: {}".format(request.GET.dict()))
        elif request.method == 'POST':
            if request.content_type.lower() == 'application/json':
                if request.FILES:
                    files = []
                    for item in request.FILES:
                        files.append(request.FILES.get(item).name)
                    log_list.append("Input: {}".format(files))
                elif hasattr(request, '_body'):
                    log_list.append("Input: {}".format(json.dumps(json.loads(request.body), ensure_ascii=False)))
        else:
            log_list.append('request method not support in logger')

        if hasattr(response, '_container'):
            log_list.append('Output: {}'.format(str(response.content, encoding='utf-8')))

        log_list.append('======================Request End======================')
        log_content = '\n'.join(log_list)
        logger.info(log_content)
        if hasattr(request, 'request_id'):
            response['X-Request-ID'] = local.request_id
        try:
            del local.request_id
        except AttributeError:
            pass
        return response
