import unittest
import logging
import io

# configure the logger
logging.basicConfig(filename='test.log', level=logging.INFO)

# create a test suite
test_suite = unittest.TestLoader().discover('.', pattern='test*.py')

# create a logger handler with a string buffer as the stream object
stream_handler = logging.StreamHandler(stream=io.StringIO())
stream_handler.setLevel(logging.INFO)
logging.getLogger().addHandler(stream_handler)

# create a test runner with the logger
test_runner = unittest.TextTestRunner(stream=stream_handler.stream, verbosity=2)

# run the test suite
test_runner.run(test_suite)

# get the log output as a string and write it to a file
log_output = stream_handler.stream.getvalue()
with open('test.log', 'w') as f:
    f.write(log_output)
