import pytest
from health_checker import HealthChecker
from health_checker import DomainStatistics


@pytest.fixture
def checker():
    return HealthChecker("input.yaml")


@pytest.fixture
def domain_stats():
    return DomainStatistics()


def test_get_domain(checker):
    assert checker.get_domain("https://fetch.com") == "fetch.com"
    assert checker.get_domain("https://www.example.com") == "www.example.com"


def test_update_domain_statistics(checker):
    checker.process_url("https://fetch.com", {})
    domain_stats = checker.domains_stats["fetch.com"]
    assert domain_stats.total_requests > 0


def test_update(domain_stats):
    domain_stats.update(True)
    domain_stats.update(False)
    assert domain_stats.total_requests == 2
    assert domain_stats.successful_requests == 1


def test_get_hit_ratio_100_percentage(domain_stats):
    domain_stats.update(True)
    domain_stats.update(True)
    assert domain_stats.get_hit_ratio() == 100.0


def test_get_hit_ratio_75_percentage(domain_stats):
    domain_stats.update(True)
    domain_stats.update(True)
    domain_stats.update(True)
    domain_stats.update(False)
    assert domain_stats.get_hit_ratio() == 75.0


def test_get_hit_ratio_50_percentage(domain_stats):
    domain_stats.update(True)
    domain_stats.update(False)
    assert domain_stats.get_hit_ratio() == 50.0


def test_get_hit_ratio_0_percentage(domain_stats):
    domain_stats.update(False)
    domain_stats.update(False)
    assert domain_stats.get_hit_ratio() == 0.0
