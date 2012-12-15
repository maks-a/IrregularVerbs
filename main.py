#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import src.singleton
import src.app


def run():
    me = src.singleton.SingleInstance()
    me
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    src.app.App()

if __name__ == '__main__':
    run()
