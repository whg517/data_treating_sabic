import logging
import os
import re
from typing import Any, Dict, List, Set, Union

import pandas as pd
import yaml

from .. import settings
from ..utils import constant
from ..utils.log import configure_logging

logger = logging.getLogger(__name__)

ConfigType = List[Dict[str, Dict[str, Union[str, Dict[str, str]]]]]

configure_logging()


class PathFactory:

    def __init__(self, date_path: str) -> None:
        self._date_path = date_path

    @property
    def base_dir(self) -> str:
        return settings.BASEDIR

    @property
    def data_dir(self) -> str:
        path = os.path.join(self.base_dir, constant.DATA_DIR, self._date_path)
        os.makedirs(path, exist_ok=True)
        return path

    @property
    def raw_file_dir(self) -> str:
        path = os.path.join(self.data_dir, constant.RAW_FILE_DIR)
        os.makedirs(path, exist_ok=True)
        return path

    @property
    def word_bag_file_dir(self) -> str:
        path = os.path.join(self.data_dir, constant.WORD_BAG_DIR)
        os.makedirs(path, exist_ok=True)
        return path

    @property
    def output_dir(self) -> str:
        path = os.path.join(self.data_dir, constant.OUTPUT_DIR)
        os.makedirs(path, exist_ok=True)
        return path


def load_config(filename: str) -> ConfigType:
    logger.debug(f'Load config file: {filename}')
    with open(os.path.join(settings.CONFIG_DIR, filename), 'r', encoding='utf-8') as file:
        config = yaml.load(file, yaml.FullLoader)
        return config


def update_config_filename_to_path(
        config: Dict[str, Any],
        file_dir: str
) -> Dict[str, Any]:
    """
    Recursive update filename field's value in config.
    :param config:
    :param file_dir:
    :return:
    """
    updated_word_config = {}
    for k, v in config.items():
        if isinstance(v, str) and k == 'filename':
            v = os.path.join(file_dir, v)
        elif isinstance(v, dict):
            # Recursive update if value is dict
            v = update_config_filename_to_path(v, file_dir)
        updated_word_config.update({k: v})
    return updated_word_config


def load_data(
        file: str,
        sheet: str,
        drop_columns: list = None
) -> pd.DataFrame:
    """
    Load excel data.
    :param file:
    :param sheet:
    :param drop_columns:
    :return:
    """
    logger.debug(f'Load data file: {file}, sheet: {sheet}')
    df = pd.read_excel(file, sheet_name=str(sheet) or 0)
    df.drop(labels=drop_columns or [], axis=1)
    df.fillna(0)
    return df


def duplicates(data: dict):
    """
    去真子集
    {"abc": 123, "bc": 456}
    :param data:
    :return:
    """
    data = {k: v for k, v in sorted(data.items(), key=lambda item: len(item[0]))}
    duplicated = {}
    for x in data.keys():
        exist = False
        for y in data.keys():
            if x.lower() == y.lower():
                continue
            if x.lower() in y.lower():
                exist = True
                break
            else:
                exist = False
        if not exist:
            duplicated.update({x: data.get(x)})
    return duplicated


__BLANK_PATTERN = re.compile(r'\s+')


def replace_blanks(data: str):
    """
    替换空白符为一个空格
    :param data:
    :return:
    """
    if data is pd.NA or data == 'nan':
        return '空'
    findall = __BLANK_PATTERN.findall(str(data))
    for i in findall:
        data = data.replace(i, ' ')
    return data


datetime_pattern = re.compile(
    r'^([2][0][0-2][0-9][-\./年]?)(((1[02]|0?[13578])[-\./月]?([12][0-9]|3[01]|0?[1-9])日?)|((11|0?[469])[-\./月]?([12][0-9]|30|0?[1-9])日?)|(0?2[-\./月]?([1][0-9]|2[0-8]|0?[1-9])日?))')  # NOQA: E501


def remove_datetime(x: str):
    # if '20190925' in x:
    #     print(x)
    if x is pd.NA or x == 'nan':
        return '空'
    x = str(x)
    x_process = []
    x = x.replace(';', '|').replace('，', '|')

    reg = True

    x_split = x.split('|')
    x_split.reverse()
    for x_i in x_split:
        x_i_sub = re.sub(r'.*：', '', x_i)

        findall = datetime_pattern.findall(x_i_sub)

        if reg:
            if findall:
                reg = False
                for group in [group for groups in findall for group in groups]:
                    x_i = x_i.replace(group, '')

        x_process.append(x_i)
    return '|'.join(x_process)


percentage_pattern = re.compile(r'(\d{1,2}\.?\d{0,2}%[~-]*)')


def remove_percentage(x: str):
    if x is pd.NA or x == 'nan':
        return '空'
    findall = percentage_pattern.findall(str(x))
    if findall:
        for i in findall:
            if i:
                x = x.replace(i, '')
    return x


grade_pattern = re.compile(r'^[A-Z]*(\d+)[A-Z]*$')


def fix_grade(x):
    if x:
        match = grade_pattern.match(x.upper())
        if match:
            return match.group(1)
    else:
        return x


recycle_pattern = re.compile(r'(非为?|不是)再生')


def process_mapping_with_quality(mappings: Dict[str, Set], *args):
    processed_data = set()

    args = '|'.join([str(i) for i in args if i is not pd.NA])
    args = args.replace('nan', '')
    for k, v in mappings.items():
        if k in args:
            if 'Recycle' in v and recycle_pattern.search(args):
                # processed_data.update(v)
                pass
            else:
                processed_data.update(v)

    return '|'.join(processed_data)
