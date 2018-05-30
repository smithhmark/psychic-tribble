
import pytest
import json

import peal

@pytest.fixture()
def big_input():
    return """{
    "restaurants": [{
        "id": "58b868503c6f4d322fa8f552",
        "version": "asdjasd",
        "address": {
            "building": "1007",
            "coord": "[­73.856077, 40.848447]",
            "street": "Morris Park Ave",
            "zipcode": "10462"
        },
        "borough": "Bronx",
        "cuisine": "Bakery",
        "grades": [{
            "date": "2014­03­03T00:00:00.000Z",
            "grade": "A",
            "score": {
                "x": 1,
                "y": 2
            }
        }, {
            "date": "2011­11­23T00:00:00.000Z",
            "grade": "A",
            "score": {
                "x": 11,
                "y": 22
            }
        }],
        "name": "Morris Park Bake Shop"
    }]
}"""

def test_spiral(big_input):
    #print(big_input)
    oo = json.loads(big_input)
    print(oo)
    outs = peal.spiral_in(oo)
    print("outs:",outs)
    assert len(outs) == 4
    assert len(outs['restaurants']) == 1
    assert len(outs['restaurants_address']) == 1
    assert len(outs['restaurants_grades']) == 2
    assert '__index' not in outs['restaurants_address']
    for ii, vv in enumerate(outs['restaurants_grades']):
        assert '__index' in vv
        assert vv['__index'] == ii
    assert len(outs['restaurants_grades_score']) == 2
    for ii, vv in enumerate(outs['restaurants_grades_score']):
        assert '__index' in vv
        assert vv['__index'] == ii

    """
    assert False
    bye = {
            'restaurants': [
                {'id': '58b868503c6f4d322fa8f552',
                    'version': 'asdjasd',
                    'borough': 'Bronx',
                    'cuisine': 'Bakery',
                    'name': 'Morris Park Bake Shop',
                    '__index': 0}],
            'restaurants_address': [
                {'id': '58b868503c6f4d322fa8f552',
                    'building': '1007',
                    'coord': '[\xad73.856077, 40.848447]',
                    'street': 'Morris Park Ave',
                    'zipcode': '10462',
                    '__index': 0}],
            'restaurants_grades': [
                {'id': '58b868503c6f4d322fa8f552',
                    '__seq': 0,
                    '__path': 'restaurants[0]_grades[0]',
                    'date': '2014\xad03\xad03T00:00:00.000Z',
                    'grade': 'A',
                    '__index': 0},
                {'id': '58b868503c6f4d322fa8f552',
                    '__seq': 1,
                    '__path':
                    'restaurants[0]_grades[1]',
                    'date': '2011\xad11\xad23T00:00:00.000Z',
                    'grade': 'A',
                    '__index': 1}],
            'restaurants_grades_score': [
                {'id': '58b868503c6f4d322fa8f552',
                    'x': 1,
                    'y': 2,
                    '__index': 0},
                {'id': '58b868503c6f4d322fa8f552',
                    'x': 11,
                    'y': 22,
                    '__index': 1}]}
    """

