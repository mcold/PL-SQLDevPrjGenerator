# coding: utf-8
import typer
import os

app = typer.Typer()

dir = ''
sep = '\\'
file_path_start = '1,4,,,'
prj_start = 'PL/SQL Developer Project'
prj_ext = 'prj'
l_accept_ext = ['sql']
token_with =''

clear = lambda: os.system('cls')
dir_name = lambda: os.path.abspath(dir).rpartition(os.sep)[-1].upper()
prj_abs_file = lambda: os.path.abspath(dir) + os.sep + dir_name() + '.' + prj_ext
prj_abs_file_token = lambda: os.path.abspath(dir) + os.sep + dir_name() + '_' + token_with.upper() + '.' + prj_ext

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

def get_prj_dir(prj_dir: str = None) -> str:
    if not os.path.exists(prj_dir):
        print('\nNot correct directory!\n\n')
        while True:
            clear()
            prj_dir = input("\nEnter directory for project: \n")
            if not os.path.exists(prj_dir): 
                continue
            else:
                print('\nNot correct directory!\n\n')
            return prj_dir
    else:
        return prj_dir        

def set_prj_dir(prj_dir: str = None):
    global dir
    dir = get_prj_dir(prj_dir)

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
@app.command(help='Full project output')
def get_prj_output(prj_dir: str):
    set_prj_dir(prj_dir = prj_dir)
    print(get_prj())

@app.command(help='Project output with files containing token')
def get_prj_output_by_token(prj_dir: str, token: str = typer.Argument(str, help="Only files with token")):
    set_prj_dir(prj_dir = prj_dir)
    print(get_prj(token = token))

@app.command(help='Project output without files containing token')
def get_output_without_token(prj_dir: str, token: str = typer.Argument(str, help="Only files without token")):
    set_prj_dir(prj_dir = prj_dir)
    print(get_prj(token_without = token))

@app.command(help='Generate project')
def gen_output(prj_dir: str):
    set_prj_dir(prj_dir = prj_dir)
    with open(prj_abs_file(), 'w') as f: f.write(get_prj(token_without=token))

@app.command(help='Generate project with files containing token')
def gen_by_token(prj_dir: str, token: str = typer.Argument(str, help="Only files with token")):
    global token_with
    token_with = token
    set_prj_dir(prj_dir = prj_dir)
    with open(prj_abs_file_token(), 'w') as f: f.write(get_prj(token=token))

@app.command(help='Generate project without files containing token')
def gen_without_token(prj_dir: str, token: str = typer.Argument(str, help="Only files without token")):
    set_prj_dir(prj_dir = prj_dir)
    with open(prj_abs_file(), 'w') as f: f.write(get_prj(token_without=token))

@app.command(help='Generate typical project')
def gen_standard(prj_dir: str):
    gen_without_token(prj_dir=prj_dir, token='rollback')

@app.command(help='Generate typical project rollback')
def gen_std_rollback(prj_dir: str):
    gen_by_token(prj_dir=prj_dir, token='rollback')

@app.command(help='Generate typical projects (full + rollback)')
def gen_def(prj_dir: str):
    gen_without_token(prj_dir=prj_dir, token='rollback')
    gen_by_token(prj_dir=prj_dir, token='rollback')

if __name__ == "__main__":
    app()