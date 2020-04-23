import logging
from typing import Dict, Set

import pandas as pd

from data_treating_sabic.utils import duplicates, load_data

logger = logging.getLogger(__name__)


def process_mapping_to_exist_col(mappings: Dict[str, Set], source, dest):
    if dest:
        return dest
    else:
        return process_mapping(source, mappings, return_rule='max')[1]


def init_mappings(filename: str, sheet, key_index, value_index):
    """
    初始化 mappings
    :return:
    """
    product_df = load_data(filename, sheet=sheet)
    logger.info(f'Start init {sheet} mapping, key index: {key_index}, value index: {value_index}......')
    return build_mappings(product_df, key_index=key_index, value_index=value_index)


def build_mappings(df: pd.DataFrame, key_index, value_index, limit=0) -> Dict[str, set]:
    """
    从 df 中构造映射数据
    index | name | addr
    ------|------|-------
      0   | foo  | beijing
      1   | bar  | shanghai
      2   |  foo | nanjing

    上数据得到 mappings

    {
        "foo" : ["beijing", "nanjing"],
        "bar" : ["shanghai"]
    }
    :param df:zx
    :param key_index:   key 对应的列索引
    :param value_index: value 对应的列索引
    :param limit:
    :return:
    """
    mappings = {}
    if limit:
        df = df.hdad(limit)
    for line in df.values:
        key = line[key_index]
        if key is pd.NA:
            key = ''
        else:
            key = str(key).lower()

        value = line[value_index]
        if value is pd.NA:
            value = ''
        else:
            value = str(value).strip()

        values = mappings.get(key)  # type:set
        if values:
            values.add(value)
        else:
            values = {value}
        mappings.update({key: values})

        if mappings.get(''):
            mappings.pop('')
    return mappings


def process_mapping(x, mappings: Dict[str, Set], rule='>', return_rule='all'):
    """
    根据 mappings 映射所有值
    :param x:
    :param mappings:
    :param rule: 匹配规则
        >: x in y 解释： x -> y
        <: y in x 解释： x <- y
        =: x==y 解释： x == y
    :param return_rule: 返回规则
        all: 返回所有
        max: 最长优先
        min: 最短优先
    :return:
    """
    # global count
    # count += 1
    # print(f'\r{count}', end='')
    if not x:
        return ''
    processed_x = {}
    for k, v in mappings.items():
        try:
            if rule == '>':
                if k.lower() in x.lower():
                    processed_x.update({k: v})
            elif rule == '<':
                if x.lower() in k.lower():
                    processed_x.update({k: v})
            elif rule == '=':
                if x.lower() == k.lower():
                    processed_x.update({k: v})
        except AttributeError:
            print(k, v)
            raise

    if not processed_x:
        return '', ''

    # 去真子集关系
    processed_x = duplicates(processed_x)

    processed_x_keys = sorted(processed_x.keys(), key=lambda i: len(i))

    if return_rule == 'max':
        processed_x_key = [processed_x_keys[-1]]
    elif return_rule == 'min':
        processed_x_key = [processed_x_keys[0]]
    else:
        processed_x_key = processed_x_keys

    return '|'.join(processed_x_key), '|'.join([i for k in processed_x_key for i in processed_x.get(k)])
