
def _cp_child(src, parent_id_field, parent_id):
    new_child = {}
    for kk, vv in src.items():
        new_child[kk] = vv
    new_child[parent_id_field] = parent_id
    return new_child

def _cp_child_list(li, parent_id_field, parent_id, seq_key='__index'):
    lo = []
    for ii, child in enumerate(li):
        cc = _cp_child(child, parent_id_field, parent_id)
        cc[seq_key] = ii
        lo.append(cc)
    return lo

def rend(oo, parent_id_field="id", seq_key='__index'):
    """ rend takes a deserialized JSON object and splits out sub-objects
    first: the JSON object
    second: the id field in the object, defaults to "id"
    returns: a tuple of the parent dictionary and a dictionary of the children 
        that were split out of the source object
    """
    new_parent = {}
    children = {}
    pid = oo.get(parent_id_field)
    for kk, vv in oo.items():
        if isinstance(vv, dict):
            children[kk] = _cp_child(vv, parent_id_field, pid)
        elif isinstance(vv, list):
            children[kk] = _cp_child_list(vv, parent_id_field, pid, seq_key)
        else:
            new_parent[kk] = vv
    return new_parent, children


def join(parent, children, parent_id_field="id"):
    merged = {}
    for kk, vv in parent.items():
        merged[kk] = vv
    for kk, vv in children.items():
        new_child = {}
        for kj, vj in vv.items():
            if kj != parent_id_field:
                new_child[kj] = vj
        merged[kk] = new_child
    return merged

def imux(lo):
    """take a list of joined objects and return lists of rent objects
    """
    lists = {}

    return lists
