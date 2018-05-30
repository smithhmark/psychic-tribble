from collections import deque

def _jn(basep, childp, path_sep='_'):
    return "{}{}{}".format(basep, path_sep, childp)

def spiral_in(obj,
        parent_id_field="id",
        path_sep='_'):
    """
    """
    family = 0
    all_objs = {}
    seq_key='__seq'
    recon_key='__path'
    work = deque()
    for base_name, subobj in obj.items(): # items in outter dict 
        if isinstance(subobj, list):
            print("list")
            for ii, li in enumerate(subobj):
                abs_path = "{}[{}]".format(base_name, ii)
                wi = abs_path, base_name, li, li.get(parent_id_field), None
                #print("q:", wi)
                work.append(wi)
        else:
            wi = base_name, base_name, subobj, subobj.get(parent_id_field), None
            work.append(wi)

    while len(work) > 0:
        rest_path, path, obj, pid, seq = work.popleft()
        #print("path:",path)
        print("path:",rest_path)
        #print("\tseq:",seq)
        #cases:
        #  list
        #  dict
        if isinstance(obj, list):
            if seq is None:
                # beginning a list bc seq is None
                if len(obj) == 0:
                    # what do do at empty sublist
                    print("encountered empty list at ", path)
                else:
                    #print("encountered list at path:{}".format( path))
                    for ii, sobj in enumerate(obj):
                        #print("\tenquing work with seq:", seq)
                        abs_path = "{}[{}]".format(rest_path, ii)
                        wi = (abs_path, path, sobj, pid, ii)
                        print("q:", wi)
                        work.append(wi)
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
                        abs_path = _jn(rest_path, kk, path_sep)
                        wi = (abs_path, _jn(path, kk, path_sep), vv, pid, None)
                        work.append(wi)
                    elif isinstance(vv, list):
                        #print("found sub list '{}' at path:{}".format(kk, path))
                        abs_path = _jn(rest_path, kk, path_sep)
                        wi = (abs_path, _jn(path, kk, path_sep), vv, pid, None)
                        work.append(wi)
                    else:
                        curr[kk] = vv
            else:
                # in a list
                curr[seq_key] = seq
                curr[recon_key] = rest_path
                for kk, vv in obj.items():
                    if isinstance(vv, dict):
                        #print("found sub item '{}' at path:{} seq:{}".format(
                            #kk, path, seq))
                        abs_path = _jn(rest_path, kk, path_sep)
                        wi = (abs_path, _jn(path, kk, path_sep), vv, pid, None)
                        #print("enq:",wi)
                        work.append(wi)
                    elif isinstance(vv, list):
                        #print("found sub list '{}' at path:{} seq:{}".format(
                            #kk, path, seq))
                        abs_path = _jn(rest_path, kk, path_sep)
                        wi = (abs_path, _jn(path, kk, path_sep), vv, pid, None)
                        work.append(wi)
                    else:
                        curr[kk] = vv
            all_objs.setdefault(path, []).append(curr)
    for vv in all_objs.values():
        if len(vv) > 1:
            for ii, ll in enumerate(vv):
                ll['__index'] = ii
    return all_objs

