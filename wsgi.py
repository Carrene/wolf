import os

from wolf import wolf

wolf.configure(files=os.environ.get('WOLF_CONFIG_FILE'))
wolf.initialize_models()

app = wolf
