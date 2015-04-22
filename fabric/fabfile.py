import os
from fabric.context_managers import show, settings, cd, prefix
from fabric.contrib import files
from fabric.operations import run, sudo, get, local, put, open_shell
from fabric.state import env
from fabric.api import task

REMOTE_REVISION = None


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

def esudo(*args, **kwargs):
    with settings(warn_only=True):
        result = sudo(*args, **kwargs)
    if result.failed:
        raise CommandFailed("args: %r, kwargs: %r, error code: %r" % (args, kwargs, result.return_code), result)
    return result


# http://docs.fabfile.org/en/latest/usage/execution.html#roles

def describe_revision(head='HEAD'):
    actual_tag = local('git describe --always --tags %s' % head, capture=True)
    return actual_tag

def get_dump_filepath(user, prefix=u'backups'):
    return '%s/%s.sql' % (prefix, get_remote_revision(user))

def get_release_filename():
    return '%s.tar.gz' % describe_revision()

def get_release_filepath():
    return 'releases/%s' % get_release_filename()

@task
def dump_db_snapshot(db_name, user):
    remote_tmp_file_path = '/tmp/dump_db.sql' # FIXME: use temporary file
    sudo('pg_dump %s > %s' % (db_name, remote_tmp_file_path), user='postgres')
    get(remote_path=remote_tmp_file_path, local_path= get_dump_filepath(user))

def reset_db():
    local('python manage.py reset_db')

@task
def load_db(user):
    local('cat %s | python manage.py dbshell' % get_dump_filepath(user))

@task
def load_db_snapshot(db_name, username):
    dump_db_snapshot(db_name, username)
    reset_db()
    load_db(username)

@task
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
    erun('source %s/bin/activate && honcho --env ../.env run ./manage.py collectstatic --noinput' % virtualenv_path)

def django_migrate(virtualenv_path):
    erun('source %s/bin/activate && honcho --env ../.env run ./manage.py migrate' % virtualenv_path)

@task
def release(head='HEAD', web_root=None, requirements=u'requirements.txt'):
    # locally we create the archive with the app code
    create_release_archive(head)
    release_filename = get_release_filename()
    # and upload it to the server
    if not files.exists(release_filename):
        put(local_path=get_release_filepath())

    cwd = erun('pwd').stdout if not web_root else web_root

    app_dir = os.path.abspath(os.path.join(cwd, 'app-%s' % describe_revision(head)))
    virtualenv_path = os.path.abspath(os.path.join(cwd, '.virtualenv'))

    try:
        # if exists remove dir
        erun('( test -d %s && rm -vfr %s ) || true' % (
            app_dir,
            app_dir,
        ))
        # create the remote dir
        erun('mkdir -p %s' % app_dir)
        erun('tar xf %s -C %s' % (
            release_filename,
            app_dir,
        ))
        sync_virtualenv(virtualenv_path, '%s/%s' % (app_dir, requirements,))# parametrize
        with cd(app_dir):
            django_collectstatic(virtualenv_path)
            django_migrate(virtualenv_path)

        erun('unlink app || true') # this fails if the first time
        erun('ln -s %s app' % app_dir)
    except CommandFailed as e:
        print 'An error occoured: %s' % e
        print '''
####################################
#        fallback to shell         #
####################################
'''
    open_shell('cd %s && source %s/bin/activate' % (
        app_dir,
        virtualenv_path,
    ))

def get_remote_revision(user):
    global REMOTE_REVISION

    if not REMOTE_REVISION:
        current_app_dir = esudo('cd && basename $(readlink -f app)', user=user)
        try:
            _, REMOTE_REVISION = current_app_dir.split('-')
        except Exception as e:
            print e
            REMOTE_REVISION = 'unknown'

    return REMOTE_REVISION

