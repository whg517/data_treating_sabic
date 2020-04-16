import logging
import os
from datetime import datetime
from typing import Dict, Union

from .utils import (PathFactory, constant, fix_grade, load_config, load_data,
                    process_mapping_with_quality, remove_datetime,
                    remove_percentage, replace_blanks,
                    update_config_filename_to_path)
from .utils.mapping import (init_mappings, process_mapping,
                            process_mapping_to_exist_col)

logger = logging.getLogger(__name__)


class Process:

    def __init__(self, date_path: str, config_file: str):
        self.date_path = date_path
        self.path_factory = PathFactory(self.date_path)
        self.configs = load_config(config_file)

    def run(self):
        for config in self.configs:
            raw_config = update_config_filename_to_path(config.get(constant.CONFIG_RAW), self.path_factory.raw_file_dir)
            word_config = update_config_filename_to_path(
                config.get(constant.CONFIG_WORD_BAG),
                self.path_factory.word_bag_file_dir
            )
            self._process(
                raw_config=raw_config,
                word_config=word_config
            )

    def _process(
            self,
            raw_config: Dict[str, str],
            word_config: Dict[str, Union[str, Dict[str, str]]]
    ):
        raw_df = load_data(os.path.join(self.path_factory.data_dir, raw_config['filename']), sheet=raw_config['sheet'])

        raw_df['规格_cleaned'] = raw_df[raw_config['col_name']] \
            .map(lambda x: replace_blanks(str(x))) \
            .map(lambda x: remove_datetime(x)) \
            .map(lambda x: remove_percentage(x))

        if word_config.get('grade'):
            mappings = init_mappings(**word_config.get('grade'))
            logger.info(f'Start processing TD_grade ......')
            raw_df['TD_grade_search'], raw_df['TD_grade'] = raw_df['规格_cleaned'].map(lambda x: x.lower()).map(
                lambda x: process_mapping(x, mappings, return_rule='max')).str

        if word_config.get('supplier'):
            mappings = init_mappings(**word_config.get('supplier'))
            logger.info(f'Start processing TD_supplier ......')
            raw_df['TD_supplier_search'], raw_df['TD_supplier'] = raw_df['规格_cleaned'].map(lambda x: x.lower()).map(
                lambda x: process_mapping(x, mappings, return_rule='max')).str

        if word_config.get('brand'):
            mappings = init_mappings(**word_config.get('brand'))
            logger.info(f'Start processing TD_brand ......')
            raw_df['TD_brand_search'], raw_df['TD_brand'] = raw_df['规格_cleaned'].map(lambda x: x.lower()).map(
                lambda x: process_mapping(x, mappings, return_rule='max')).str

        if word_config.get('quality'):
            mappings = init_mappings(**word_config.get('quality'))
            logger.info(f'Start processing TD_Quality ......')
            raw_df['TD_Quality'] = raw_df.apply(
                lambda line: process_mapping_with_quality(mappings, line['产品名称'], line['规格']), axis=1)

        if word_config.get('grade_to_supplier'):
            mappings = init_mappings(**word_config.get('grade_to_supplier'))
            logger.info(f'Start processing grade_to_supplier ......')
            raw_df['TD_supplier'] = raw_df.apply(
                lambda line: process_mapping_to_exist_col(mappings,
                                                          line['TD_grade'],
                                                          line['TD_supplier']),
                axis=1)

        if word_config.get('grade_to_brand'):
            mappings = init_mappings(**word_config.get('grade_to_brand'))
            logger.info(f'Start processing grade_to_brand ......')
            raw_df['TD_brand'] = raw_df.apply(
                lambda line: process_mapping_to_exist_col(mappings,
                                                          line['TD_grade'],
                                                          line['TD_brand']),
                axis=1)

        if word_config.get('brand_to_supplier'):
            mappings = init_mappings(**word_config.get('brand_to_supplier'))
            logger.info(f'Start processing brand_to_supplier ......')
            raw_df['TD_supplier'] = raw_df.apply(
                lambda line: process_mapping_to_exist_col(mappings,
                                                          line['TD_brand'],
                                                          line['TD_supplier']),
                axis=1)

        if word_config.get('fix_grade'):
            raw_df['fix_grade'] = raw_df['TD_grade'].map(lambda x: str(x).lower()).map(
                lambda x: fix_grade(x))

        now = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = raw_config["filename"]
        filename_prefix = os.path.basename(filename).split('.')[0]

        raw_df.to_excel(os.path.join(self.path_factory.output_dir, f'{filename_prefix}-{now}.xlsx'), index=False)
