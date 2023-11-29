import os

class Utils:


    @staticmethod
    def getRootPath():
        # 获取当前Python脚本的绝对路径
        current_file = os.path.abspath(__file__)

        # 获取当前脚本所在目录的路径
        current_dir = os.path.dirname(current_file)

        # 递归向上查找，直到找到包含项目特定文件（例如，requirements.txt，或其他项目标识文件）的目录
        while not os.path.exists(os.path.join(current_dir, 'requirements.txt')):
            current_dir = os.path.dirname(current_dir)

        # 最终的current_dir就是项目的根目录
        project_root = current_dir
        return project_root
