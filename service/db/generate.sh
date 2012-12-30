#!/bin/sh

sqlautocode mysql://robot_wr:robot_wr@localhost/Magazines -d -o models/raw/__init__.py
