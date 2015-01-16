import os
from fabric.context_managers import show, settings, cd, prefix
from fabric.contrib import files
from fabric.operations import run, sudo, get, local, put, open_shell
from fabric.state import env


# https://gist.github.com/lost-theory/1831706
class CommandFailed(Exception):
    def __init__(self, message, result):
        Exception.__init__(self, message)
        self.result = result

def erun(*args, **kwargs):
    with settings(warn_only=True):
        result = run(*args, **kwargs)
    if result.failed:
        raise CommandFailed("args: %r, kwargs: %r, error code: %r" % (args, kwargs, result.return_code), result)
    return result

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

def sync_virtualenv(virtualenv_path, requirements_path):
    if not files.exists(virtualenv_path):
        erun('virtualenv --no-site-packages %s' % virtualenv_path)

    erun('source %s/bin/activate && pip install -r %s' % (
        virtualenv_path,
        requirements_path,
    ))

def virtualenv(virtualenv_path, *args, **kwargs):
    prefix('source %s/bin/activate' % virtualenv_path)

def django_collectstatic(virtualenv_path):
    erun('source %s/bin/activate && honcho --env ../.env run ./manage.py collectstatic' % virtualenv_path)

def release(head='HEAD'):
    cwd = erun('pwd').stdout
    create_release_archive(head)
    release_filename = get_release_filename()
    if not files.exists(release_filename):
        put(local_path=get_release_filepath())

    app_dir = 'app-%s' % describe_revision(head)
    virtualenv_path = os.path.abspath(os.path.join(cwd, '.virtualenv'))

    try:
        # create the remote dir
        erun('mkdir -p %s' % app_dir)
        erun('tar xf %s -C %s' % (
            release_filename,
            app_dir,
        ))
        sync_virtualenv(virtualenv_path, '%s/requirements/staging.txt' % app_dir)# parametrize
        with cd(app_dir):
            django_collectstatic(virtualenv_path)
    except CommandFailed as e:
        print 'An error occoured: %s' % e
        print '''
####################################
#        fallback to shell         #
####################################
'''
    open_shell()