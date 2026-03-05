import json
import os

def save_data(file_path, data):
    """TODO: 实现序列化并写入 JSON"""
    pass

def load_data(file_path):
    """TODO: 实现从 JSON 读取并重建对象"""
    if not os.path.exists(file_path):
        return []
    pass