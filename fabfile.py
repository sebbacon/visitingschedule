from fabric.api import run
from fabric.api import prefix, warn, abort
from fabric.api import task, env
from fabric.contrib.files import exists
from fabric.context_managers import cd



env.hosts = ['smallweb1.ebmdatalab.net']
env.forward_agent = True
env.colorize_errors = True
env.user = 'root'

environments = {
    'live': 'visitingschedule',
}


def make_directory():
    run('mkdir -p %s' % (env.path))


def venv_init():
    run('[ -e venv ] || python3.5 -m venv venv')


def pip_install():
    with prefix('source venv/bin/activate'):
        run('pip install -q -r visitingschedule/requirements.txt')


def update_from_git():
    # clone or update code
    if not exists('visitingschedule/.git'):
        run("git clone -q https://github.com/sebbacon/visitingschedule.git")
    else:
        with cd("visitingschedule"):
            run("git pull -q")


def setup_nginx():
    run('ln -sf %s/visitingschedule/deploy/supervisor-%s.conf /etc/supervisor/conf.d/%s.conf' % (env.path, env.app, env.app))
    run('ln -sf %s/visitingschedule/deploy/nginx-%s /etc/nginx/sites-enabled/%s' % (env.path, env.app, env.app))
    run('chown -R www-data:www-data /var/www/%s/{visitingschedule,venv}' % (env.app))
    run('service supervisor restart')
    run('nginx -t && service nginx stop && service nginx start')


def run_migrations():
    if env.environment == 'live':
        with prefix('source venv/bin/activate'):
            run('cd visitingschedule && python manage.py migrate --settings=visitingschedule.settings')
    else:
        warn("Refusing to run migrations in staging environment")



@task
def deploy(environment, branch='master'):
    if environment not in environments:
        abort("Specified environment must be one of %s" %
              ",".join(environments.keys()))
    env.app = environments[environment]
    env.environment = environment
    env.path = "/var/www/%s" % env.app
    env.branch = branch

    make_directory()
    with cd(env.path):
        venv_init()
        update_from_git()
        pip_install()
        run_migrations()
        setup_nginx()
