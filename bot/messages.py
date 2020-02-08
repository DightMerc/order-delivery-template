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

    }
