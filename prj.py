# coding: utf-8
import typer
from typing import Optional
import os

app = typer.Typer()

dir = "C:\\Users\\mholo\\WD\\SQL\\zmmm_04443"
sep = '\\'
file_path_start = '1,4,,,'
prj_start = 'PL/SQL Developer Project'
l_accept_ext = ['sql']


def is_exists_by_token(l_str: list, token: str = None, token_without: str = None) -> bool:
    if not token and not token_without: return True
    for str_name in l_str:
        if token:
            if str_name.lower().find(token.lower()) < 0:
                continue
        if token_without:
            if str_name.lower().find(token_without.lower()) > 0:
                continue
        return True
    return False

def get_groups(token: str = None, token_without: str = None) -> list:
    s_groups = set()
    for f in os.walk(dir):
        try:
            if is_exists_by_token(f[2], token=token, token_without=token_without): s_groups.add(f[0].replace(dir, '').split('\\')[1])
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
    return '\n'.join(get_order_files(get_files(token = token, token_without = token_without)))

def get_order_files_header_str(token: str = None, token_without: str = None) -> str:
    return '\n'.join(['[Files]', get_order_files_str(token=token, token_without=token_without)]) 

def get_files_order(l_files: list, group_name: str) -> str:
    l_num = list()
    for i in range(len(l_files)):
        f_path = l_files[i]
        if f_path.lower().startswith(group_name.lower() + '\\'): l_num.append(i)
    return ','.join([str(x) for x in l_num])


def get_order_groups(l_groups: list, token: str = None, token_without: str = None) -> list:
    l_files = get_files(token=token, token_without=token_without)
    l_gr_str = list()
    l_gr_str.sort()
    for gr in l_groups: l_gr_str.append(gr.upper() + '=' + get_files_order(l_files, gr) + ',')
    return l_gr_str

def get_order_groups_str(token: str = None, token_without: str = None) -> str:
    l_gr_str = get_order_groups(get_groups(token=token, token_without=token_without), token=token, token_without=token_without)
    l_gr_str.sort()
    return '\n'.join(l_gr_str)

def get_order_groups_header_str(token: str = None, token_without: str = None):
    return '\n'.join(['[Groups]', get_order_groups_str(token=token, token_without=token_without)])


def get_prj(token: str = None, token_without: str = None) -> str:
    return '\n\n'.join([prj_start, get_order_groups_header_str(token=token, token_without=token_without), get_order_files_header_str(token=token, token_without=token_without)])


############## Application ####################################
## TODO: add dir argument
@app.command(help='Full project output')
def get_prj_output():
    print(get_prj())

## TODO: add dir argument
@app.command(help='Project output with files containing token')
def get_prj_output_by_token(token: str = typer.Argument(str, help="Only files with token")):
    print(get_prj(token = token))

## TODO: add dir argument
@app.command(help='Project output without files containing token')
def get_prj_output_without_token(token: str = typer.Argument(str, help="Only files without token")):
    print(get_prj(token_without = token))


## TODO: add dir argument
@app.command(help='Generate project')
def gen_prj_output():
    # print(get_prj())
    pass

## TODO: add dir argument
@app.command(help='Generate project with files containing token')
def gen_prj_by_token(token: str = typer.Argument(str, help="Only files with token")):
    # print(get_prj(token = token))
    pass

## TODO: add dir argument
@app.command(help='Generate project without files containing token')
def gen_prj_without_token(token: str = typer.Argument(str, help="Only files without token")):
    # print(get_prj(token_without = token))
    pass

## TODO: standard project

## TODO: standard rollback project

# @app.command()
# def main(name: str = typer.Argument(str, help="The name of the user to greet")):
#     print(f"Hello {name}")


if __name__ == "__main__":
    app()
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
    # print(get_prj(token='rollback'))
    # print(get_prj(token_without='rollback'))