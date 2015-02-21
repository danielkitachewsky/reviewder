
import unittest
import sys


def main():
  import optparse
  parser = optparse.OptionParser()
  parser.add_option('-v', '--verbose', dest='verbose', default=False,
                    help='Verbose output', action='store_true')

  options, args = parser.parse_args()

  verbosity = 1
  if options.verbose:
      verbosity = 2

  loader = unittest.loader.TestLoader()
  test = loader.discover(".", "*_test.py")
  runner = unittest.runner.TextTestRunner(verbosity=verbosity)
  result = runner.run(test)
  sys.exit(not result.wasSuccessful())

if __name__ == '__main__':
  main()
