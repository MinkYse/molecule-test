import os

import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('hostA')

def test_postgresql_installed(host):
    assert host.package("postgresql").is_installed, "PostgreSQL не установлен на сервере."
    assert host.service("postgresql").is_running, "Служба PostgreSQL не запущена на сервере."

def test_nginx_access_restrictions(host):
    #inventory = testinfra.utils.ansible_runner.AnsibleRunner(
    #    os.environ["MOLECULE_INVENTORY_FILE"]
    #)
    #hostB = inventory.get_hosts("hostB")
    #hostB_facts = inventory.run_module(hostB[0], "setup", [])
    #hostB_ip = hostB_facts["ansible_facts"]["ansible_default_ipv4"]["address"]
    nginx_cmd = f'curl -I http://hostB/'
    nginx_cmd_2 = f'curl -I https://hostB/'
    # Проверка, что Nginx на hostB недоступен с hostA
    result = host.run(nginx_cmd)
    result2 = host.run(nginx_cmd_2)
    assert result2.rc != 0, f"Доступ к Nginx на сервере hostB с hostA не был закрыт."

def test_postgres_firewall(host):
    inventory = testinfra.utils.ansible_runner.AnsibleRunner(
        os.environ["MOLECULE_INVENTORY_FILE"]
    )
    hostB = inventory.get_hosts("hostB")
    hostB_facts = inventory.run_module(hostB[0], "setup", [])
    hostB_ip = hostB_facts["ansible_facts"]["ansible_default_ipv4"]["address"]
    iptables_rules = host.iptables.rules('filter', 'INPUT')
    port_5432_rule_from_hostB_renue = f'-A INPUT -s {hostB_ip}/32 -p tcp -m tcp --dport 5432 -j ACCEPT'
    port_5432_rule_not_from_hostB_renue = '-A INPUT -p tcp -m tcp --dport 5432 -j DROP'
    assert port_5432_rule_from_hostB_renue in iptables_rules, 'Доступ с хоста B открыт или не ограничен'
    assert port_5432_rule_not_from_hostB_renue in iptables_rules, 'Доступ с других хостов открыт'
