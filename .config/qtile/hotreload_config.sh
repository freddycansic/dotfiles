#!/bin/bash

reload_config_if_valid() {
  if /home/freddy/qtile-env/bin/python /home/freddy/.config/qtile/config.py; then
    /home/freddy/qtile-env/bin/qtile cmd-obj -o cmd -f reload_config
    echo "reloaded config"
  fi
}

while inotifywait -e modify /home/freddy/.config/qtile/*.py &> /dev/null; do reload_config_if_valid; done;
