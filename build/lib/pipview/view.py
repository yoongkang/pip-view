import os
import subprocess

from pip.basecommand import Command
from pip.commands.show import search_packages_info
from pip.status_codes import SUCCESS, ERROR
from pip._vendor import pkg_resources


class ViewCommand(Command):

    """
    Views the package source directory with the editor defined in
    $PIP_EDITOR.
    """
    name = 'view'
    usage = """
      %prog <package>"""
    summary = 'View installed package in the editor'

    def __init__(self, *args, **kw):
        super(ViewCommand, self).__init__(*args, **kw)

    def run(self, options, args):
        if not args:
            return ERROR
        if not os.getenv('PIP_EDITOR'):
            return ERROR
        query = args
        shell_command = os.getenv('PIP_EDITOR').split()
        results = list(search_packages_info(query))
        installed = dict(
            [(p.project_name.lower(), p) for p in pkg_resources.working_set])
        if len(results) is 0:
            return ERROR
        for dist in results:
            pkg = installed[dist['name'].lower()]
            names = list(pkg.get_metadata_lines('top_level.txt'))
            for i in range(len(names)):
                fullpath = os.path.join(dist['location'], names[i])
                if os.path.isdir(fullpath):
                    names[i] = fullpath
                elif os.path.isfile(fullpath + '.py'):
                    names[i] = fullpath + '.py'
                elif os.path.isfile(fullpath + '.so'):
                    names[i] = fullpath + '.so'
                else:
                    return ERROR
            status_code = subprocess.call(shell_command + names)
            if status_code is not SUCCESS:
                return ERROR
        return SUCCESS


def main(*args):
    view_cmd = ViewCommand()
    view_cmd.run({}, args)
