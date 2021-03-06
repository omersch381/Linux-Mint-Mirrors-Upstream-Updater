from mirrors_manager import MirrorsManager
from arg_parser import ArgParser
from logger import Logger

logger = Logger(__name__)
logger = logger.logger

args = ArgParser().parse_args()
logger.debug(f'Args which were received are:\n{args}')

mirrors_manager = MirrorsManager(args)
mirrors_manager.run()
