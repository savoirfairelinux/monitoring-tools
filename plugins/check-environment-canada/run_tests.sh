#!/bin/bash

wheel_house="/tmp/wheelhouse"

rm -rf env
virtualenv env
source env/bin/activate

pip install --upgrade pip nose setuptools wheel

pip wheel --find-links=${wheel_house} --wheel-dir=${wheel_house} .

# pip install --use-wheel --find-links=${wheel_house} -e .[test]
# don't know but this fail on jenkins@sflphonebuild-ubuntu12 with :
cat << END >/dev/null
 Obtaining file:///home/jenkins/workspace/monitoring-tools/plugins/check-environment-canada
  Exception:
  Traceback (most recent call last):
    File "/home/jenkins/workspace/monitoring-tools/plugins/check-environment-canada/env/local/lib/python2.7/site-packages/pip/basecommand.py", line 232, in main
      status = self.run(options, args)
    File "/home/jenkins/workspace/monitoring-tools/plugins/check-environment-canada/env/local/lib/python2.7/site-packages/pip/commands/install.py", line 339, in run
      requirement_set.prepare_files(finder)
    File "/home/jenkins/workspace/monitoring-tools/plugins/check-environment-canada/env/local/lib/python2.7/site-packages/pip/req/req_set.py", line 436, in prepare_files
      req_to_install.extras):
    File "/home/jenkins/workspace/monitoring-tools/plugins/check-environment-canada/env/local/lib/python2.7/site-packages/pip/_vendor/pkg_resources/__init__.py", line 2504, in requires
      "%s has no such extra feature %r" % (self, ext)
  UnknownExtra: Unknown 1.0 has no such extra feature 'test'
END
# So I just do :
pip install --use-wheel --find-links=${wheel_house} -r requirements.txt

(cd tests && nosetests) && rm -rf env
