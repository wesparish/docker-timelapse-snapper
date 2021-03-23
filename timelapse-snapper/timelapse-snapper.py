#!/usr/bin/env python3

from lib.snapper import Snapper

from optparse import OptionParser
from prometheus_client import Gauge, start_http_server
from threading import Event

import datetime
import logging
import os
import sys
import time

exit = Event()

logging.basicConfig(stream=sys.stdout, level=getattr(logging, os.getenv('TIMELAPSE_SNAPPER_LOG_LEVEL', 'INFO')))

parser = OptionParser()
parser.add_option('-u', '--img-url', dest='img_url',
                  default=os.getenv('TIMELAPSE_SNAPPER_IMG_URL'),
                  help='image URL (TIMELAPSE_SNAPPER_IMG_URL)')
parser.add_option('-p', '--img-save-path',
                  default=os.getenv('TIMELAPSE_SNAPPER_IMG_SAVE_PATH', '.'),
                  help='Image save path (TIMELAPSE_SNAPPER_IMG_SAVE_PATH, default: .)')
parser.add_option('-r', '--img-prefix',
                  default=os.getenv('TIMELAPSE_SNAPPER_IMG_PREFIX', 'snapshot'),
                  help='Image prefix (TIMELAPSE_SNAPPER_IMG_PREFIX, default: snapshot)')
parser.add_option('-i', '--snapshot-interval', type = "int",
                  default=os.getenv('TIMELAPSE_SNAPPER_SNAPSHOT_INTERVAL', '60'),
                  help='Snapshot interval in seconds (TIMELAPSE_SNAPPER_IMG_PREFIX, default: 60)')
(options, args) = parser.parse_args()

print("options: %s" % options)

start_http_server(9000, addr='0.0.0.0')
total_snaps = Gauge('total_snaps', 'Total downloaded snapshots')

if not options.img_url:
  print("img_url is required!")
  parser.print_help()
  sys.exit(1)

def main():
    snapper = Snapper(options.img_url,
                      options.img_save_path,
                      options.img_prefix)
    while not exit.is_set():
      saved_snap_file = snapper.download_snap()
      total_snaps.inc()
      logging.info("Successfully saved snap: %s" % (saved_snap_file))

      logging.info("Sleeping for %s seconds" % options.snapshot_interval)
      exit.wait(options.snapshot_interval)

    print("Exiting gracefully")

def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    exit.set()

if __name__ == '__main__':
    import signal
    for sig in ('TERM', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG'+sig), quit);
    main()