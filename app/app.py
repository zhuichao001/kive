#!/usr/bin/python 
#-*- coding:utf-8 -*-

import re
from kive.common.singleton import *


@singleton
class App():
    def __init__(self):
        self.routes = []

    @staticmethod
    def build_route_pattern(route):
        route_regex = re.sub(r'(<\w+>)', r'(?P\1.+)', route)
        return re.compile("^{0}$".format(str(route_regex)))

    def route(self, route_str):
        def decorator(f):
            route_pattern = self.build_route_pattern(route_str)
            self.routes.append((route_pattern, f))
            return f
        return decorator

    def get_route_match(self, path):
        for route_pattern, view_function in self.routes:
            m = route_pattern.match(path)
            if m:
                return m.groupdict(), view_function
        return None

    def serve(self, path):
        route_match = self.get_route_match(path)
        if route_match:
            kwargs, view_function = route_match
            return view_function(**kwargs)
        else:
            raise ValueError('Route "{0}"" has not been registered'.format(path))

app = App()
