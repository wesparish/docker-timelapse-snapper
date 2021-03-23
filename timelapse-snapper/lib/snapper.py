#!/usr/bin/env python3
import time
import logging
import os
import requests
import sys

logging.basicConfig(stream=sys.stdout, level=getattr(logging, os.getenv('TIMELAPSE_SNAPPER_LOG_LEVEL', 'INFO')))

class Snapper:
  def __init__(self,
               img_url,
               image_save_path=".",
               image_prefix = "snapshot"):
    self._img_url = img_url
    self._image_save_path = image_save_path
    self._image_prefix = image_prefix

    try:
      os.makedirs(self._image_save_path)
    except FileExistsError:
      pass

  def download_snap(self):
    output_file = "%s_%s" % (self._image_prefix, time.strftime("%Y-%m-%d-%H:%M:%S"))

    # Download image from URL
    logging.info("Getting snapshot from URL: %s" % (self._img_url))
    r = requests.get(self._img_url, allow_redirects=True)
    output_file += "." + r.headers.get('Content-Type').split('/')[1]
    with open("%s/%s" % (self._image_save_path, output_file), "wb") as outfile:
      outfile.write(r.content)
    
    return "%s/%s" % (self._image_save_path, output_file)

import unittest
class TestSnapper(unittest.TestCase):
  def setUp(self):
    pass
  def tearDown(self):
    pass

  def test_Google(self):
    img_url = "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
    expected_file_name = time.strftime("google_%Y-%m-%d-%H:%M:%S.png")
    Snapper(img_url, "/dev/shm/test_Google", "google").download_snap()

    test_image = "%s/test_data/google.png" % (os.path.dirname(os.path.realpath(__file__)))

    import filecmp
    assert(filecmp.cmp('/dev/shm/test_Google/%s' % expected_file_name, test_image))

if __name__ == "__main__":
  unittest.main(verbosity=2)