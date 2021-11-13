#!/bin/bash

SCRIPTS=/home/jason/workspace/happygarden/remote

cd $SCRIPTS
python state_check.py > >(logger -t coop -p user.info) 2> >(logger -t coop -p user.info)
