# -*- coding: utf-8 -*-

name = 'nemomaya'

version = '0.0.1'

description = 'Nemo Maya API'

authors = ['WuZhen']

tools = []

requires = []

def commands():
    '''
    '''
    env.MAYA_MODULE_PATH.append('{root}')

format_version = 2
