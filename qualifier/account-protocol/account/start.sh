#!/bin/bash

nsjail -Ml --port 7777 --user 9999 --group 9999 --time_limit 30 --chroot /jail -- account