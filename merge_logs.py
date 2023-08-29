from json import loads, dump, decoder

import time
import sys

from datetime import datetime
from pathlib import Path

_FORMAT = "%Y-%m-%d %H:%M:%S"


def _merge_logs(log_a_dir: Path, log_b_dir: Path, log_result_dir: Path) -> None:
    try:
        with open(log_a_dir) as log_a, open(log_b_dir) as log_b, open(log_result_dir, 'w') as log_res:
            print('merging log files...')

            temp_dict_a = loads(log_a.readline())
            cur_line_a = datetime.strptime(temp_dict_a['timestamp'], _FORMAT)
            temp_dict_b = loads(log_b.readline())
            cur_line_b = datetime.strptime(temp_dict_b['timestamp'], _FORMAT)

            while True:
                if cur_line_a != "" and cur_line_b != "":

                    if cur_line_a < cur_line_b:
                        dump(temp_dict_a, log_res)
                        log_res.write('\n')
                        try:
                            temp_dict_a = loads(log_a.readline())
                            cur_line_a = datetime.strptime(temp_dict_a['timestamp'], _FORMAT)
                        except decoder.JSONDecodeError:
                            cur_line_a = ""

                    else:
                        dump(temp_dict_b, log_res)
                        log_res.write('\n')
                        try:
                            temp_dict_b = loads(log_b.readline())
                            cur_line_b = datetime.strptime(temp_dict_b['timestamp'], _FORMAT)
                        except decoder.JSONDecodeError:
                            cur_line_b = ""

                elif cur_line_a == "" and cur_line_b != "":
                    dump(temp_dict_b, log_res)
                    log_res.write('\n')
                    try:
                        temp_dict_b = loads(log_b.readline())
                        cur_line_b = datetime.strptime(temp_dict_b['timestamp'], _FORMAT)
                    except decoder.JSONDecodeError:
                        cur_line_b = ""

                elif cur_line_b == "" and cur_line_a != "":
                    dump(temp_dict_a, log_res)
                    log_res.write('\n')
                    try:
                        temp_dict_a = loads(log_a.readline())
                        cur_line_a = datetime.strptime(temp_dict_a['timestamp'], _FORMAT)
                    except decoder.JSONDecodeError:
                        cur_line_a = ""

                else:
                    break

    except FileNotFoundError:
        print('Пожалуйста, введите правильные пути к файлам!')


def main() -> None:
    log_a_dir, log_b_dir, log_result_dir = [sys.argv[i] for i in [1, 2, 4]]

    t0 = time.time()
    log_a_dir = Path(log_a_dir)
    log_b_dir = Path(log_b_dir)
    log_result_dir = Path(log_result_dir)
    _merge_logs(log_a_dir, log_b_dir, log_result_dir)
    print(f'finished in {time.time() - t0} sec')


if __name__ == "__main__":
    main()
