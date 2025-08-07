import sys
import os

def change_file_name(file_path, new_name):
    """Change the file name to the new name."""
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return False
    
    directory = os.path.dirname(file_path)
    new_file_path = os.path.join(directory, new_name)
    try:
        os.rename(file_path, new_file_path)
        print(f"File renamed to {new_file_path}")
        return True
    except Exception as e:
        print(f"Error renaming file: {e}")
        return False

def has_sub_dir(path):
    """
    检查指定路径下是否有两重子文件夹
    
    Args:
        path (str): 要检查的文件夹路径
    
    Returns:
        bool: 如果有两重子文件夹返回True，否则返回False
    """
    if not os.path.exists(path) or not os.path.isdir(path):
        print(f"路径 {path} 不存在或不是文件夹")
        return False
    
    try:
        # 遍历第一层子目录
        for item1 in os.listdir(path):
            item1_path = os.path.join(path, item1)
            
            # 检查是否是文件夹
            if os.path.isdir(item1_path):
                # 遍历第二层子目录
                for item2 in os.listdir(item1_path):
                    item2_path = os.path.join(item1_path, item2)
                    
                    # 如果第二层也有文件夹，说明有两重子文件夹
                    if os.path.isdir(item2_path):
                        return True
        
        return False
        
    except PermissionError:
        print(f"没有权限访问路径 {path}")
        return False
    except Exception as e:
        print(f"检查路径时出错: {e}")
        return False


def has_sub_dir_with_details(path):
    """
    检查指定路径下是否有两重子文件夹，并返回详细信息
    
    Args:
        path (str): 要检查的文件夹路径
    
    Returns:
        tuple: (bool, list) - (是否有两重子文件夹, 两重子文件夹路径列表)
    """
    if not os.path.exists(path) or not os.path.isdir(path):
        return False, []
    
    two_level_dirs = []
    
    try:
        for item1 in os.listdir(path):
            item1_path = os.path.join(path, item1)
            
            if os.path.isdir(item1_path):
                for item2 in os.listdir(item1_path):
                    item2_path = os.path.join(item1_path, item2)
                    
                    if os.path.isdir(item2_path):
                        two_level_dirs.append(item2_path)
        
        return len(two_level_dirs) > 0, two_level_dirs
        
    except Exception as e:
        print(f"检查路径时出错: {e}")
        return False, []


if __name__ == "__main__":
    print("This script is not meant to be run directly.")