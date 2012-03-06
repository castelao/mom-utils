#!/usr/bin/env python
# -*- coding: Latin-1 -*-
# vim: tabstop=4 shiftwidth=4 expandtab


import yaml
import re


def nml_decode(text):
    """
    """
    output = []
    text = re.sub("\t", " ", text)

    # dummy way to deal with comments. Need to improve it
    text = re.sub("\s*!.*\n", "\n", text)

    for namelists in re.findall("&((?:.*\n)+?)\s*/", text):
        g = re.match("\s*(?P<groupname>\w+)\n((?:.*\n)*)", namelists).groups()
        output.append("%s:\n" % g[0])
        #for p in re.findall("\s+(\w+)\s*=\s*(\.?.*\.?)\s*,?\s*(!.*)\n", g[1]):
        for p in re.findall("\s*(\w+)\s*=\s*(\.?.*\.?)\s*,?\s*\n", g[1]):
            tmp = re.sub(",$|\s*", "", p[1])
            if tmp == ".false." or tmp == '.FALSE.':
                tmp = False
            if tmp == ".true." or tmp == '.TRUE.':
                tmp = True
            output.append("  %s: %s\n" % (p[0], tmp))
    textout = "".join(output)
    return yaml.load(textout)

# Working on
#group_pattern = """
#(&\s*
#(?P<groupname>\w+).*\n
#(.*\n)+
#)
#"""
#re.search(group_pattern, text, re.VERBOSE).groups()


def yaml2nml(cfg, key_order=None):
    """
    """
    output = []
    keys = cfg.keys()

    if key_order:
        key_order = list(key_order)
        if set(key_order) <= set(keys):
            key_order += (set(keys) - set(key_order))
        else:
            raise KeyError
    else:
        key_order = sorted(keys)

    for k in key_order:
        output.append(" &%s\n" % k)
        if cfg[k] != None:
            parameters = cfg[k].keys()
            parameters.sort()
            for kk in parameters:
                v = cfg[k][kk]
                if v is False:
                    v = '.FALSE.'
                elif v is True:
                    v = '.TRUE.'
                else:
                    try:
                        if abs(int(v) - float(v)) == 0:
                            v = int(v)
                        else:
                            v = float(v)
                    except ValueError:
                        try:
                            v = float(v)
                        except ValueError:
                            try:
                                v.split(',')[1]
                            except ValueError:
                                v = "'%s'" % v
                            except IndexError:
                                v = "'%s'" % v
                            else:
                                v = "%s" % v
                output.append("    %s = %s,\n" % (kk, v))
        output.append("/\n\n")
    return "".join(output)
