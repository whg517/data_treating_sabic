from data_treating_sabic.sabic import Process

if __name__ == '__main__':
    """
    This date_str variable is your date path, please modify.
    This config_filename is your configuration for this process in config directory. Not full path
    Note: It is one layer directory name. Such as /data/20150521/raw, you should set `date_str = '20150521'`,
    do not set `date_str = '/data/20100521/raw'`. We can not get correct data file is you set full path.
    """
    date_str = '20200416'
    config_filename = '20200416.yml'
    processor = Process(date_str, config_filename)
    processor.run()
