
def rend(oo, parent_id_field="id"):
    """
    """
    new_parent = {}
    children = {}
    for kk, vv in oo.items():
        if isinstance(vv, dict):
            new_child = {}
            for kj, vj in vv.items():
                new_child[kj] = vj
            new_child[parent_id_field] = oo.get(parent_id_field)
            children[kk] = new_child
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
