#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author: QJane
from django import template

from account.forms import LoginForm
from account.forms import UserMessageForm


register = template.Library()


@register.assignment_tag
def get_login_form():
    return LoginForm(prefix='login_form')


@register.assignment_tag
def get_message_form():
    return UserMessageForm()
