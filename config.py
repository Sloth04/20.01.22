import sys
import logging
from pathlib import Path
from logging import StreamHandler, Formatter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--day',
                    help='enter day, format YYYY-MM-DD',
                    action='store',
                    default='2022-01-19')

args = parser.parse_args()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

output = Path.cwd() / 'output'
input_dir = Path.cwd() / 'input'
edited_data_mask = args.day[2:].replace('-', '.')
look_for_mask = f'{edited_data_mask}*_uts_fcr_*.csv'
output.mkdir(parents=True, exist_ok=True)

DATABASE_NAME = 'FCR'
