from place import Place

def test_get_update_statement():
    place = Place(42, 'foo', 'N52.000', 'E15.000', None)
    place.get_update_statements()
