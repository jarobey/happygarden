#!/bin/bash

SCRIPTS=/home/pi/workspace/happygarden/remote

cd $SCRIPTS
python3 local_state_check.py > >(logger -t coop -p user.info) 2> >(logger -t coop -p user.info)
