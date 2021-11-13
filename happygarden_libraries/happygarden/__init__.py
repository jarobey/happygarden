import logging, getopt, sys, pickle
from pathlib import Path

VERSION = "0.7"

# TODO Wrap this properly--currently useful for debugging.
try:
    opts, args = getopt.getopt(sys.argv[1:], None, ["log_level=","home_dir","cache_dir="])
except getopt.GetoptError as err:
    # print help information and exit:
    print(err) # will print something like "option -a not recognized"
    sys.exit(2)
log_level = logging.WARNING
home_dir = Path.home() / '.happygarden'
cache_dir = home_dir / 'cache'
for o, a in opts:
    if o == "--log_level":
        log_level_str = a
        log_level = getattr(logging, log_level_str.upper(), None)
    if o == "--home_dir":
        home_dir = Path(a)
    if o == "--cache_dir":
        cache_dir = Path(a)
home_dir.mkdir(exist_ok=True)
cache_dir.mkdir(exist_ok=True)

if not isinstance(log_level, int):
    raise ValueError('Invalid log level: %s' % log_level_str)
logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def save_object(object_to_save, file_path):
    logger.debug('Saving to {1}'.format(object_to_save, file_path))
    with file_path.open(mode='wb') as f:
        pickle.dump(object_to_save, f)

def load_object(file_path):
    rtn = None
    if file_path.exists():
        logger.debug('Reading file {0}'.format(file_path))
        with file_path.open(mode='rb') as f:
            rtn = pickle.load(f)
    else: logger.debug("Can't load object.  {0} doesn't exist".format(file_path))
    return rtn