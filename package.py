# -*- coding: utf-8 -*-

name = 'nemomaya'

version = '0.0.10'

description = 'Nemo Maya Client'

authors = ['wuzhen']

tools = []

requires = []

def commands():
    '''
    '''
    env.MAYA_MODULE_PATH.append('{root}')

format_version = 2
