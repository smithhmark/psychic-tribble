from collections import deque

def _jn(basep, childp, path_sep='_'):
    return "{}{}{}".format(basep, path_sep, childp)

def spiral_in(obj,
        parent_id_field="id",
        path_sep='_',
        seq_key='__seq'):
    """
    """
    family = 0
    all_objs = {}
    work = deque()
    for base_name, subobj in obj.items(): # items in outter dict 
        if isinstance(subobj, list):
            for ii in subobj:
                work_item = base_name, ii, ii.get(parent_id_field), None
                work.append(work_item)
        else:
            work_item = base_name, subobj, subobj.get(parent_id_field), None
            work.append(work_item)

    while len(work) > 0:
        path, obj, pid, seq = work.popleft()
        #print("path:",path)
        #print("\tseq:",seq)
        #cases:
        #  list
        #  dict
        if isinstance(obj, list):
            if seq is None:
                # beginning a list bc seq is None
                if len(obj) == 1:
                    # ignore list part and skip to child
                    #print("single elt list at", path)
                    work.append((path, obj[0], pid, None))
                elif len(obj) == 0:
                    # what do do at empty sublist
                    print("encountered empty list at ", path)
                else:
                    #print("encountered list at path:{}".format( path))
                    for ii, sobj in enumerate(obj):
                        #print("\tenquing work with seq:", seq)
                        work.append((path, sobj, pid, ii))
            else:
                # a sub list in the middle of a list?
                print("encountered the start of a sublist in list at", path)
                #print("\t seq:{}".format(seq))
        elif isinstance(obj, dict):
            #print("copying:", path)
            curr = {parent_id_field: pid}
            if seq is None:
                # not in a list
                for kk, vv in obj.items():
                    if isinstance(vv, dict):
                        #print("found sub item '{}' at path:{}".format(kk, path))
                        work.append((_jn(path, kk, path_sep), vv, pid, None))
                    elif isinstance(vv, list):
                        #print("found sub list '{}' at path:{}".format(kk, path))
                        work.append((_jn(path, kk, path_sep), vv, pid, None))
                    else:
                        curr[kk] = vv
            else:
                # in a list
                curr[seq_key] = seq
                for kk, vv in obj.items():
                    if isinstance(vv, dict):
                        #print("found sub item '{}' at path:{} seq:{}".format(
                            #kk, path, seq))
                        wi = (_jn(path, kk, path_sep), vv, pid, None)
                        #print("enq:",wi)
                        work.append(wi)
                    elif isinstance(vv, list):
                        #print("found sub list '{}' at path:{} seq:{}".format(
                            #kk, path, seq))
                        work.append((_jn(path, kk, path_sep), vv, pid, None))
                    else:
                        curr[kk] = vv
            #print("storing copy")
            all_objs.setdefault(path, []).append(curr)
            #all_at_path = all_objs.get(path, [])
            #all_at_path.append(curr)
    for vv in all_objs.values():
        if len(vv) > 0:
            for ii, ll in enumerate(vv):
                ll['__index'] = ii
    return all_objs

