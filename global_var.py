from protocol_config import *

global _global_dict


def init():
    global _global_dict
    _global_dict = {'protocol_config': protocol_config(), 'length_constraints': {}, 'good_lc': [], 'lc_count': 0,
                    'mem': [], 'filter_length_constraints': [], 'finish_dfs_idx': []}


def get_lc():
    return _global_dict['length_constraints']


def get_lc_count():
    return _global_dict['lc_count']


def set_lc_count(count):
    _global_dict['lc_count'] = count


def get_good_lc():
    return _global_dict['good_lc']


def get_mem():
    return _global_dict['mem']


def get_flc():
    return _global_dict['filter_length_constraints']


def get_fdi():
    return _global_dict['finish_dfs_idx']

