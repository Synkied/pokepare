"""
Fabric deployment tasks

To use, please install dependencies

$ pip install fabric
"""


from datetime import datetime

from fabric.api import cd
from fabric.api import env
from fabric.api import execute
from fabric.api import lcd
from fabric.api import local
from fabric.api import roles
from fabric.api import run
from fabric.api import settings
from fabric.api import shell_env
from fabric.api import task
from fabric.contrib.project import rsync_project


# Default version to be used for release.
default_version = '1.1-%s' % datetime.now().strftime('%Y-%m-%d-%H-%M')

# Defines the roles (ssh user/host) to be used on fabric tasks.
env.roledefs = {
    'production': ['quentin@188.166.108.19']
}

REMOTE_SRV_DIR = '/home/quentin/pokepare_project/'
REMOTE_APP_DIR = '/home/quentin/pokepare_project/frontend/'
REMOTE_PUBLIC_DIR = '%sdist' % REMOTE_SRV_DIR


@task
def gitflow_release(version=None):
    """
    Creates a git flow release https://bit.ly/2sLZtaJ
    """
    if version is None:
        version = input('Version [%s]: ' % default_version)
        if not version.strip():
            version = default_version

    with shell_env(GIT_MERGE_AUTOEDIT='no'):
        local('git fetch origin -p')
        local('git checkout develop')
        local('git merge --ff-only origin/develop')
        local('git checkout master')
        local('git merge --ff-only origin/master')
        local('git flow release start v%s' % version)
        local('git flow release finish -m v%s v%s' % (version, version))
        local('git checkout develop')


@task
def local_push_tags():
    """
    Locally push tags to origin/develop and origin/master.
    """
    local('git push origin develop master --tags')


@task
def update_remote_branch(branch, host):
    """
    Remotely pull specified branch and merge it with its origin counterpart.
    """
    with cd(REMOTE_SRV_DIR):
        run('git fetch origin -p')
        run('git checkout -f %s' % branch)
        run('git merge --ff-only origin/%s' % branch)

    print('\x1b[0;30;42mUpdate success for %s@%s !\x1b[0m' % (
            host, branch
        )
    )


@task
@roles('production')
def remote_install_production(release=None):
    """
    Installs newly added packages.
    """
    with cd(REMOTE_APP_DIR):
        run('yarn install')


@task
@roles('production')
def remote_pull_production(release=None):
    """
    Sets branch to release or 'master' and calls update_remote_branch.
    """
    branch = release or 'master'
    update_remote_branch(branch, 'production')


@task
def local_build_production():
    """
    Locally builds the app to be served on production.
    """
    with lcd('$HOME/dev/pokepare/'):
        local('make yarn_build')


@task
@roles('production')
def local_transfer_production_to_remote(release=None):
    """
    Rsync transfer local build to remote production machine.
    """
    rsync_project(REMOTE_PUBLIC_DIR, local_dir="./dist/", delete=True)


@task
@roles('production')
def remote_restart_production(release=None):
    """
    Remotely restart production pm2 service.
    """
    with cd(REMOTE_SRV_DIR):
        run('make restart')


@task
def mep(version=None):
    """
    Total deploy on production (app & server).
    Git flow release + local build production +
    transfer production build to remote + remote git pull origin master +
    remote restart production
    """
    gitflow_release(version)
    execute(local_push_tags)
    execute(local_build_production)
    execute(local_transfer_production_to_remote)
    execute(remote_pull_production)
    execute(remote_restart_production)


@task
def mep_install(version=None):
    """
    Total deploy on production (app & server).
    Git flow release + local build production +
    transfer production build to remote + remote git pull origin master +
    remote restart production
    """
    gitflow_release(version)
    execute(local_push_tags)
    execute(local_build_production)
    execute(local_transfer_production_to_remote)
    execute(remote_pull_production)
    execute(remote_install_production)
    execute(remote_restart_production)


@task
def mep_no_build(version=None):
    """
    Total deploy on production, no build (uses old 'public/' build).
    Git flow release + transfer production build to remote +
    remote git pull origin master + remote restart production
    """
    gitflow_release(version)
    execute(local_push_tags)
    execute(local_transfer_production_to_remote)
    execute(remote_pull_production)
    execute(remote_restart_production)


@task
def mep_no_build_no_transfer(version=None):
    """
    Partial deploy on production, no build and no app transfer.
    Git flow release + remote git pull origin master +
    remote restart production
    """
    gitflow_release(version)
    execute(local_push_tags)
    execute(remote_pull_production)
    execute(remote_restart_production)


@task
def mep_app(version=None):
    """
    Partial deploy on production (app only).
    Git flow release + local build production +
    transfer production build to remote + remote restart production
    """
    gitflow_release(version)
    execute(local_push_tags)
    execute(local_build_production)
    execute(local_transfer_production_to_remote)
    execute(remote_restart_production)
