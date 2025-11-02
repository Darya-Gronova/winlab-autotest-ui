import pytest

@pytest.fixture(autouse=False)
def send_analytics_data():
    ...

@pytest.fixture(scope="session")
def settings():
    ...

@pytest.fixture(scope="class")
def user():
    ...

@pytest.fixture(scope="function")
def browser():
    ...