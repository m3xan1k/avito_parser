#!/usr/bin/env python3

l = [{'name': 'bart', 'age': 18}, {'name': 'homer', 'age': 16}, {'name': 'moe', 'age': 28}]

l_sorted = sorted(l, key = lambda x: x['name'])

print(l_sorted)
