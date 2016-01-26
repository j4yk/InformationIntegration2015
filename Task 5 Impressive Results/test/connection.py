import pytest
import pg8000

@pytest.fixture(scope='module')
def conn():
    import os
    from configparser import ConfigParser
    config = ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'test-database.ini'))
    try:
        return pg8000.connect(**config['integrated-database'])
    except KeyError:
        raise Exception("You must supply database credentials in test/test-database.ini")
