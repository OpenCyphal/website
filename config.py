import os
import sys

DEBUG = 'debug' in (x.lower() for x in sys.argv)

# A common general assumption is using 2 per available processor cores - to handle
# incoming requests using one and performing background operations using the other.
THREADS_PER_PAGE = 2
