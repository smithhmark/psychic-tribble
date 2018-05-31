from collections import deque
import os
import sys
import json

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
    for base_name, subobj in obj.items(): # items in outer dict 
        if isinstance(subobj, list):
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
        #print("path:",rest_path)
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
                        #print("q:", wi)
                        work.append(wi)
            else:
                # a sub list in the middle of a list?
                print("encountered the start of a sublist in list at", path)
                #print("\t seq:{}".format(seq))
        elif isinstance(obj, dict):
            #print("copying:", path)
            curr = {parent_id_field: pid,
                    recon_key: rest_path,
                    }
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
                #curr[seq_key] = seq
                #curr[recon_key] = rest_path
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

def split_file(path):
    with open(path, 'r') as infil:
        indata = json.load(infil)
        outs = spiral_in(indata)
        base_dir = os.path.dirname(path)
        for kk, vv in outs.items():
            opath = os.path.join(base_dir, "{}.json".format(kk))
            with open(opath, 'w') as ofil:
                json.dump(vv, ofil, indent=4)

def _step_idx(raw_step):
    splitpt = raw_step.find('[')
    step = raw_step[:splitpt]
    idx = raw_step[splitpt+1:-1]
    return step, int(idx)

def _insert_item(new_parent, item, found_in):
    #print("\nitem to insert:",item)
    path = item.get('__path')
    if path is None:
        #print(new_parent)
        #print(item)
        path = found_in
    #print("path at which to insert:",path)
    path_steps = path.split("_")
    curloc = new_parent
    for step in path_steps[1:]:
        if step.endswith(']'):
            step, idx = _step_idx(step)
            if step in curloc:
                if idx == len(curloc[step]):
                    curloc[step].append({})
                    curloc = curloc[step][-1]
                elif idx < len(curloc[step]):
                    curloc = curloc[step][idx]
                else:
                    print("ack(2), rcvd out of order list elements")
                    return
            else:
                curloc[step]=[]
                if idx == len(curloc[step]):
                    curloc[step].append({})
                    curloc = curloc[step][-1]
                else:
                    print("ack, rcvd out of order list elements")
                    return
        else:
            if step in curloc:
                if isinstance(curloc, dict):
                    curloc = curloc[step]
                else:
                    print("ugggg, adding to something that isn't a dict")
                    return
            else:
                curloc[step] = {}
                curloc = curloc[step]

    #print("inserting into:", curloc)
    for kk, vv in item.items():
        if kk not in ('__index', '__path', 'id'):
            curloc[kk] = vv

def _flesh_out(new_parent, order, dicts):
    for typ in order:
        for item in dicts[typ]:
            _insert_item(new_parent, item, typ)
    return new_parent

def reconstruct(ins, parent_id_field='id'):
    approx_order = sorted(ins.keys())
    indexes = {k:0 for k in approx_order}
    #print(approx_order)
    #print(indexes)
    out = {}
    working_on = 0
    done = False
    done = True
    for outer in ins[approx_order[0]]:
        out[approx_order[0]] = []
        new_parent = {k:v for (k,v) in outer.items() if k != '__path'}
        #print("made new toplevel obj:", new_parent)
        pid = new_parent.get(parent_id_field)
        pieces = {}
        for child_type in approx_order[1:]:
            pieces[child_type] = []
            for curidx in range(indexes[child_type], len(ins[child_type])):
                if ins[child_type][curidx].get(parent_id_field) == pid:
                    pieces[child_type].append(ins[child_type][curidx])
                else:
                    break
            indexes[child_type] = curidx
        out[approx_order[0]].append(_flesh_out(new_parent, approx_order[1:], pieces))
    return out

def join_files(opath, ipaths):
    ins = {}
    print(ipaths)
    for path in ipaths:
        name = os.path.basename(path)[:-len('.json')]
        print("reading:", path)
        #print("reading:", name)
        with open(path, 'r') as ifil:
            oo = json.load(ifil)
            ins[name] = oo
    merged_entities = reconstruct(ins)
    with open(opath, 'w') as ofil:
        print("writing:", opath)
        json.dump(merged_entities, ofil, indent=4)

def main():
    if len(sys.argv) < 2:
        print("Error, too few args: need a path to a file")
        sys.exit(1)
    elif len(sys.argv) == 2:
        ipath = sys.argv[1]
        #print(ipath)
        split_file(ipath)
    elif len(sys.argv) >= 3 and  sys.argv[1] == 'join':
        opath = sys.argv[2]
        ipaths = []
        for fp in sys.argv[3:]:
            if fp.endswith(".json"):
                ipaths.append(fp)
            else:
                print("skipping unknown commandline paramter:", fp)
        join_files(opath, ipaths)
    else:
        print("don't understand arguments")
        print("usage 1: <cmd> <filename> -> splits json-file filename into files")
        print("usage 2: <cmd> join <output_filename> <filenames> -> joins json-files into output_filename")
        sys.exit(1)

if __name__ == '__main__':
    main()
