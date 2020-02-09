#!/usr/bin/env python
# -*- coding: utf-8 -*-
import client


def Messages(user):

    lan = client.getUserLanguage(user)

    return {
        'start': client.getMessage(1, lan),
        'main': client.getMessage(2, lan),
        'menu': client.getMessage(3, lan),
        'subMenu': client.getMessage(4, lan),
        'descriptionProduct': client.getMessage(5, lan),
        'productAdded': client.getMessage(6, lan),
        'cartEmpty': client.getMessage(7, lan),
        'productRemoved': client.getMessage(8, lan),
        'name': client.getMessage(9, lan),
        'phone': client.getMessage(10, lan),
        'delivery': client.getMessage(11, lan),
        'outTime': client.getMessage(12, lan),
        'payment': client.getMessage(13, lan),
        'setTime': client.getMessage(14, lan),
        'choosePaySystem': client.getMessage(15, lan),
        'pay': client.getMessage(16, lan),
    }
