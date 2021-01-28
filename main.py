import os
import sys


def prepare_files(directory_path, mv_name='new'):

    file_list = os.listdir(directory_path)
    new_file_list = []

    top_num = int(file_list[0].split('n')[1])
    # 获取顶层文件序号
    for file in file_list:
        tmp = file.split('n')
        if int(tmp[1]) > top_num:
            top_num = int(tmp[1])
    print(top_num)

    # 处理原文件列表
    for num in range(top_num+1):
        for item in file_list:
            if int(item.split('n')[1]) == num:
                new_file_list.append(item)

    # 处理同名文件
    if mv_name == 'new' and os.path.exists('./new.ts'):
        os.remove('./new.ts')
    elif mv_name != 'new' and os.path.exists(f'./{mv_name}.ts'):
        os.remove(f'./{mv_name}.ts')

    # 读取和输出
    mv = open(f'./{mv_name}.ts', 'ab')

    for item in new_file_list:
        fd_item = open(directory_path+item, 'rb')
        content = fd_item.read()
        fd_item.close()
        mv.write(content)
    mv.close()



    pass


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <directory path > [name of movie]")
        return -1

    if len(sys.argv) == 2:
        res = os.path.exists(sys.argv[1])
        if not res:
            print('Error while loading path,Is it exists?')
            return -1
        else:
            if not os.path.isdir(sys.argv[1]):
                print('Check the path just input, Is it a directory path?')
                return -1

    if len(sys.argv) == 3:
        prepare_files(sys.argv[1], sys.argv[2])
    else:
        prepare_files(sys.argv[1])


if __name__ == '__main__':
    if main() == -1:
        print("Program running error")
