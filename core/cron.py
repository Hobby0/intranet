# -*- coding: utf-8 -*-
#
# Copyright (c) 2017 - 2018, doudoudzj
# All rights reserved.
#
# Intranet is distributed under the terms of the (new) BSD License.
# The full license can be found in 'LICENSE'.

"""Package for cron management."""

import os
import shlex
import subprocess

# from configloader import (loadconfig, raw_loadconfig, raw_saveconfig, readconfig, saveconfig, writeconfig)

CRON_DIR = '/etc/cron.d/'
CRONTAB = '/etc/crontab'

CRON_CONFIG_MAP = {
    'SHELL': 'shell',
    'MAILTO': 'mailto',
    'HOME': 'home',
    'PATH': 'path'
}


def load_config():
    try:
        if not os.path.exists(CRONTAB):
            return {}
    except OSError:
        return {}

    config = {}
    with open(CRONTAB, 'r') as f:
        lines = f.readlines()

    while len(lines) > 0:
        line = lines.pop(0)
        out = line.strip()
        if not out or out.startswith('#'):
            continue

        k = out.strip().split('=')[0]
        if k and CRON_CONFIG_MAP.has_key(k):
            config[CRON_CONFIG_MAP[k]] = out.split('=')[1]

    return config


def update_config(configs):
    cmap_reverse = dict((v, k) for k, v in CRON_CONFIG_MAP.iteritems())
    new_config = {}
    for k, v in configs.iteritems():
        if cmap_reverse.has_key(k):
            new_config[cmap_reverse[k]] = v
    return save_config(CRONTAB, new_config)


def save_config(filepath, config):
    try:
        if not os.path.exists(filepath):
            return False
    except OSError:
        return False

    with open(filepath, 'r') as f:
        lines = f.readlines()

    output = []
    while len(lines) > 0:
        line = lines.pop(0)
        out = line.strip()
        if not out or out.startswith('#'):
            output.append('%s' % (line))
            continue

        k = out.split('=')[0]
        if k:
            if config.has_key(k):
                output.append('%s=%s\n' % (k, config[k]))
            else:
                output.append('%s' % (line))

    with open(filepath, 'w') as f:
        f.writelines(output)
        return True

    return False


def listCron():
    p = subprocess.Popen(['crontab', '-l'],
                         #  stdout=subprocess.PIPE,
                         #  stderr=subprocess.PIPE,
                         close_fds=True)
    # p.stdout.read()
    # p.stderr.read()
    return p.wait() == 0


if __name__ == "__main__":
    # print CRONTAB
    # print listCron()
    # os.system("top")
    # print loadconfig(CRONTAB, CRON_CONFIG_MAP)
    # print raw_loadconfig(CRONTAB)
    print load_config()
    # print update_config({'shell': 'shelshelshel', 'home': 'homehomehome', 'path':'abc'})
    # print dict((v, k) for k, v in CRON_CONFIG_MAP.iteritems())
