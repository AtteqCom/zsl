#!/bin/sh

sqlautocode mysql://robot_wr:robot_wr@localhost/sportkynew -d -o models/raw/models.py -t state,sport,sport_club,sport_club_field,image,gallery,gallery_image,resource
