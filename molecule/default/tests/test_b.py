import os

import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('hostB')



def test_nginx_is_installed(host):
    nginx = host.package("nginx")
    assert nginx.is_installed, 'nginx не установлен'

def test_nginx_running_and_enabled(host):
    nginx = host.service("nginx")
    assert nginx.is_running, 'nginx не запущен'
    assert nginx.is_enabled

def test_nginx_prosy(host):
    curl_cmd = 'curl -I http://localhost/'

    result = host.run(curl_cmd)
    assert result.rc == 0, "Проверка переадресации завершилась с ошибкой."
    assert "Location: https://renue.ru" in result.stdout, "Переадресация не произошла на https://renue.ru." 

@pytest.mark.parametrize("database", [
    "app",
    "custom",
])
def test_postgresql_databases_exist(host, database):
    cmd = f'psql "host=hostA port=5432 user=app dbname=app password=app" -tac "\l" | grep {database}'
    result = host.run(cmd)
    assert result.rc == 0, f'База данных {database} не существует в PostgreSQL.'

@pytest.mark.parametrize("username,databases,permission", [
    ('app', ['app'], 'CTc'),
    ('custom', ['custom'], 'CTc'),
])
def test_postgresql_users_and_permissions(host, username, databases, permission):
    # Имя пользователя PostgreSQL
    perms_cmd = f'psql "host=hostA port=5432 user=app dbname=app password=app" -tac "\l" | grep {username}={permission}'
    assert host.run(perms_cmd).rc == 0, f"Пользователь {username} не имеет прав доступа {permission} к базе данных {database}."
