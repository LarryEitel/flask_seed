from utils import myyaml
import models

def run(yaml_path, uc_file, uc_key):
    fname = yaml_path + uc_file + '.yaml'
    try:
	usecases = myyaml.pyObj(fname)
    except:
	raise Exception('Failed to load yaml: ' + fname)

    uc_dat = {}
    for yamlname in ['cnt', 'prs']:
	fname = yaml_path + yamlname + '.yaml'
	try:
	    uc_dat[yamlname] = myyaml.pyObj(fname)
	except:
	    raise Exception('Failed to load yaml: ' + fname)

    uc_cmds = usecases[uc_key]

    cmds = []
    # loop through all commands for a usecase
    for cmd in uc_cmds:
	action = cmd[0]
	_cls = cmd[1]
	model_class = getattr(models, _cls)
	slug = cmd[2]

	# get data for this item
	doc_dict = uc_dat[_cls.lower()][slug]

	# if a count value, use it to repeat else 1
	cmd_count = cmd[3] if len(cmd)>3 else 1
	for i in range(cmd_count):
	    if action == 'add':
		doc = model_class(**doc_dict)
		doc.save()
		assert doc.id
		cmd.append({'doc':doc})
		cmds.append(cmd)

    return cmds