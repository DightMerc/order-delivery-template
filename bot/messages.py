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


    }
