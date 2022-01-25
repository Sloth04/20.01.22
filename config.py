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
parser.add_argument('-st', '--station',
                    help='enter station',
                    action='store',
                    default='KHAR5CHPP')
parser.add_argument('-bl', '--block',
                    help='enter block',
                    action='store',
                    default='bl2')

args = parser.parse_args()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)

output = Path.cwd() / 'output'
input_dir = Path.cwd() / 'input'
# handle command
edited_data_mask = args.day[2:].replace('-', '.')
look_for_mask = f'{edited_data_mask}_uts_fcr_*{args.station}_{args.block}'
output.mkdir(parents=True, exist_ok=True)

# df_n_columns = [
#     'datetime',
#     'generator_name',
#     'p_sum_value',
#     'power_fcr_value',
#     'statizm_value',
#     'frequency_value',
#     'delF',
#     'FCR_solution']

P_nom_KHAR5CHPP = 120
frequency_nom = 50
d1 = 0.01

DATABASE_NAME = 'FCR'
