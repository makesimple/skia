#!/usr/bin/env python
#
# Copyright 2016 Google Inc.
#
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.


"""Create the asset and upload it."""


import argparse
import common
import os
import subprocess
import sys
import utils


def main():
  if sys.platform != 'win32':
    print >> sys.stderr, 'This script only runs on Windows.'
    sys.exit(1)
  parser = argparse.ArgumentParser()
  parser.add_argument('--gsutil')
  parser.add_argument('--sdk_path', '-s', required=True)
  parser.add_argument('--runtime_path', '-r',
      default=os.path.join("C:","System32","vulkan-1.dll"),
      required=True)
  args = parser.parse_args()

  with utils.tmp_dir():
    cwd = os.getcwd()
    create_script = os.path.join(common.FILE_DIR, 'create.py')
    upload_script = os.path.join(common.FILE_DIR, 'upload.py')

    try:
      cmd = ['python', create_script,
             '-t', cwd,
             '--sdk_path', args.sdk_path,
             '--runtime_path', args.runtime_path]
      subprocess.check_call(cmd)
      cmd = ['python', upload_script, '-t', cwd]
      if args.gsutil:
        cmd.extend(['--gsutil', args.gsutil])
      subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
      # Trap exceptions to avoid printing two stacktraces.
      sys.exit(1)


if __name__ == '__main__':
  main()
