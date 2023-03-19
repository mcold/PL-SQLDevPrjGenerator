# coding: utf-8
import typer
import os

app = typer.Typer()

dir = "C:\\Users\\mholo\\WD\\SQL\\zmmm_04443"
sep = '\\'
file_path_start = '1,4,,,'
prj_start = 'PL/SQL Developer Project'
l_accept_ext = ['sql']

# TODO: get groups where exists token "rollback"!
def get_groups() -> list:
    s_groups = set()
    for f in os.walk(dir):
        try:
            s_groups.add(f[0].replace(dir, '').split('\\')[1])
        except IndexError:
            pass
    return [x for x in s_groups]

def get_path(path: str) -> str:
    try:
        return path[len(dir):]
    except IndexError:
        return None

def is_acceptable_ext(file: str) -> bool:
    for ext in l_accept_ext:
        if file.lower().endswith('.' + ext.lower()) > 0: return True
    return False


def get_files(token: str = None, token_without: str = None) -> list:
    l_files = list()
    for d in os.walk(dir):
        for f in d[2]:
            if token:
                if f.lower().find(token.lower()) < 0:
                    continue
            if token_without:
                    if f.lower().find(token_without.lower()) > 0:
                        continue
            path = get_path(d[0])
            if path and is_acceptable_ext(f):
                l_files.append(path.strip('\\') + sep + f)
            else:
                if is_acceptable_ext(f): l_files.append(f)
    return l_files            


def get_order_files(l_file_path: list) -> list:
    return [file_path_start + x for x in l_file_path]

def get_order_files_str(token: str = None, token_without: str = None) -> str:
    # TODO: change to argument
    return '\n'.join(get_order_files(get_files(token = token, token_without = token_without)))

def get_files_order(l_files: list, group_name: str) -> str:
    l_num = list()
    for i in range(len(l_files)):
        f_path = l_files[i]
        if f_path.lower().startswith(group_name.lower() + '\\'): l_num.append(i)
    return ','.join([str(x) for x in l_num])


def get_order_groups(l_groups: list) -> list:
    l_files = get_files(token_without='rollback')
    l_gr_str = list()
    l_gr_str.sort()
    for gr in l_groups: l_gr_str.append(gr.upper() + '=' + get_files_order(l_files, gr) + ',')
    return l_gr_str

def get_order_groups_str():
    l_gr_str = get_order_groups(get_groups())
    l_gr_str.sort()
    return '\n'.join(l_gr_str)

def get_order_groups_header_str():
    return '\n'.join(['[Groups]', get_order_groups_str()])


def get_prj(token: str = None, token_without: str = None) -> str:
    return '\n\n'.join([prj_start, get_order_groups_header_str(), get_order_files_str(token=token, token_without=token_without)])



if __name__ == "__main__":
    # populate_dir()
    # print(get_groups())
    # print(get_files())

    # print(get_files())
    # with open('res.txt', 'w') as f:
    #     for ff in get_files():
    #         f.write(ff + '\n')

    # main project
    # print(get_files(token_without = 'rollback'))
    # print(get_groups())
    # print(get_order_files_str())

    # rollback project
    # print(get_files(token = 'rollback'))
    # print(get_order_groups(get_groups()))

    # header groups
    # print(get_order_groups_header_str())

    # print(get_prj(token_without='rollback'))
    print(get_prj(token='rollback'))