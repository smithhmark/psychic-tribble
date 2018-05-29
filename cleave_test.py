import pytest
import io

import json

import cleave


@pytest.fixture()
def single_small():
    return """{ "id": "1234",
    "name": {
        "given": "John",
        "sur": "Doe"
        },
    "address": {
        "street": "1 Dr Carlton B Goodlett Pl",
        "city": "San Francisco",
        "state": "CA",
        "zip": "94102"
        },
    "ranking": 1024
}"""

@pytest.fixture()
def ss_file(single_small):
    return io.StringIO(single_small)

def test_rend(single_small):
    #print(single_small)
    oo = json.loads(single_small)
    print("="*10)
    print(oo)
    print("="*10)
    parent, children = cleave.rend(oo)
    print(parent)
    print(children)
    assert len(children) == 2
    assert len(parent) == 2
    assert "ranking" in parent
    assert parent['ranking'] == 1024
    assert "id" in parent
    assert parent['id'] == "1234"
    assert "name" in children
    assert 'given' in children['name']
    assert 'sur' in children['name']
    assert 'id' in children['name']
    assert children['name']['given'] == 'John'
    assert "address" in children

def test_join():
    pass
