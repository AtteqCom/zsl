#!/bin/sh

sqlautocode mysql://robot_wr:robot_wr@localhost/Magazines -d -o models/raw/__init__.py -t state,sport,sport_club,sport_club_field
