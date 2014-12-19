from StringIO import StringIO
from fabric.context_managers import show
from fabric.contrib import files
from fabric.operations import run, sudo, get, local, put, open_shell
from fabric.state import env

# http://docs.fabfile.org/en/latest/usage/execution.html#roles

def describe_revision(head='HEAD'):
    actual_tag = local('git describe --always --tags %s' % head, capture=True)
    return actual_tag

def get_dump_filepath():
    return 'backups/staging-%s.sql' % describe_revision()

def get_release_filename():
    return '%s.tar.gz' % describe_revision()

def get_release_filepath():
    return 'releases/%s' % get_release_filename()

def dump_db(db_name):
    remote_tmp_file_path = '/tmp/dump_db.sql'
    sudo('pg_dump %s > %s' % (db_name, remote_tmp_file_path), user='postgres')
    get(remote_path=remote_tmp_file_path, local_path= get_dump_filepath())

def reset_db():
    local('python manage.py reset_db')

def load_db():
    local('cat %s | python manage.py dbshell' % get_dump_filepath())

def load_db_snapshot():
    dump_db()
    reset_db()
    load_db()

def create_release_archive(head='HEAD'):
    local('git archive --worktree-attributes --format=tar.gz %s > %s' % (
        head,
        get_release_filepath()
    ))

def release(head='HEAD'):
    create_release_archive(head)
    if not files.exists(get_release_filename()):
        put(local_path=get_release_filepath())

    # tar zxvf 959fbcb.tar.gz  -C app-1bbcf18/
    open_shell()