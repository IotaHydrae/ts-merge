import os
import sys

def m3u8_auto_locator(directory_path):
    """
    定位m3u8文件
    :param directory_path:
    :return: 与目录相关的m3u8文件的绝对路径
    """
    file_list = os.listdir(directory_path)  # 指定目录文件列表
    file_name_m3u8 = ''  # m3u8文件名
    ab_path_m3u8 = ''  # m3u8文件绝对路径


    # 尝试在指定目录中 寻找m3u8文件
    for file in file_list:
        try:
            tmp = file.split('.')
            if tmp[-1] == 'm3u8':
                print("已定位到m3u8文件")
                file_name_m3u8 = file
                ab_path_m3u8 = os.getcwd() + '\\' + directory_path + file_name_m3u8
                return ab_path_m3u8
        except:
            pass

    # print(file_name_m3u8)

    # 未在指定目录 中找到m3u8文件，尝试寻找上层与目录同名的m3u8文件
    if file_name_m3u8 == '':
        directory_path_name = directory_path.split('\\')[1]
        father_directory = os.listdir(f'{directory_path}../')
        # print(directory_path_name.split('.m3u8_contents'))
        for file in father_directory:
            file_name_without_suffix = file[0:-5]  # 文件名无后缀
            directory_name_prefix = directory_path_name.split('.m3u8_contents')[0]  # 目录名前缀

            if file_name_without_suffix == directory_name_prefix:
                file_name_m3u8 = file

        ab_path_m3u8 = os.getcwd() + '\\' + file_name_m3u8  # 合成绝对路径
        return ab_path_m3u8


def m3u8_parser(directory_path,m3u8_path='None'):
    """

    :param directory_path:
    :return:
    """
    ab_path_m3u8 = m3u8_auto_locator(directory_path)
    if m3u8_path != 'None':
        ab_path_m3u8 = m3u8_path

    # 解析
    m3u8_fd = open(ab_path_m3u8, 'r')
    m3u8_content = m3u8_fd.read()
    m3u8_content_line_list = m3u8_content.split('\n')

    formatted_ts_list = []
    for line in m3u8_content_line_list:
        if line != '' and line[0] != '#':
            formatted_ts_list.append(line)

    try:
        # 处理ts路径，转换为文件名
        result_list = []
        for line in formatted_ts_list:
            result_list.append(line.split('/')[-1])

    except Exception as e:
        print(e)
        return formatted_ts_list

    return result_list
    pass


def combine_ts_files(directory_path, mv_name='new'):
    """

    :param directory_path:
    :param mv_name:
    :return:mv_path
    """

    # 解析目录中m3u8文件
    result_ts_list = m3u8_parser(directory_path)

    # 文件的读取与写入
    try:
        chose = ''
        if os.path.exists(f'./{mv_name}.ts'):
            chose = input(f"文件 {mv_name}.ts 已存在，是否覆盖？[y/n]")
            if chose == 'y':
                os.remove(f"./{mv_name}.ts")
            elif chose == 'n':
                mv_name = input("请输入新文件名(带后缀ts): ")
                mv_name = mv_name.split('.')[0]
            else:
                raise AttributeError
    except AttributeError as result:
        print("无效输入，程序退出中")
        exit()

    mv = open(f'./{mv_name}.ts', 'ab')

    for item in result_ts_list:
        print(f"读取文件中: {directory_path + item}")
        fd_item = open(directory_path + item, 'rb')
        content = fd_item.read()
        fd_item.close()
        mv.write(content)
    mv.close()
    return os.getcwd()+"\\"+mv_name
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
        output_path = combine_ts_files(sys.argv[1], sys.argv[2])
        print(f"已写入到文件: {output_path}.ts")
    else:
        output_path = combine_ts_files(sys.argv[1])
        print(f"已写入到文件: {output_path}.ts")


if __name__ == '__main__':
    if main() == -1:
        print("Program running error")
        exit()

    print("程序运行完毕")
