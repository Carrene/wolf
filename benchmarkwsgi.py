import os
import sys

from werkzeug.contrib.profiler import ProfilerMiddleware, MergeStream

from wolf import wolf

wolf.configure(files='benchmark.yml')
wolf.initialize_models()


f = open('profiler.log', 'w')
stream = MergeStream(sys.stdout, f)
app = ProfilerMiddleware(wolf, stream)
