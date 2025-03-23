# Author:  Martin McBride
# Created: 2023-05-14
# Copyright (C) 2023, Martin McBride
# License: MIT

import unittest
loader = unittest.TestLoader()
start_dir = './'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)