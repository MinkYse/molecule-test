import os

import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_devops_exist(host):
    devops = host.user('devops')
    assert devops.exists, 'Пользователя devops существует'

def test_devops_sudo_without_password(host):
    username = 'devops'
    command = f'sudo -n -l -U {username}'
    result = host.run(command)
    assert result.succeeded, f'Доступа к sudo без пароля нет'

def test_ssh_without_password(host):
    assert host.file('/etc/ssh/sshd_config').contains('PasswordAuthentication no'), 'Аутентификация по паролю не отключена'
