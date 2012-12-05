from utils import myyaml
import models

class UseCase():
    '''Convenient tools for automatically loading sample data from yaml files'''
    def __init__(self, yaml_path):
        self.yaml_path = yaml_path

    def load(self, uc_file):
        fname = self.yaml_path + uc_file + '.yaml'
        try:
            usecases = myyaml.pyObj(fname)
        except:
            raise Exception('Failed to load yaml: ' + fname)

        uc_dat = {}
        for yamlname in ['cnt', 'prs']:
            fname = self.yaml_path + yamlname + '.yaml'
            try:
                uc_dat[yamlname] = myyaml.pyObj(fname)
            except:
                raise Exception('Failed to load yaml: ' + fname)

        self.uc_dat  = uc_dat
        self.usecases = usecases

    def run_all(self, uc_key):
        cmds = []
        # loop through all commands for a usecase
        for cmd in self.usecases[uc_key]:
            cmds.append(self.run(cmd))

        return cmds


    def run(self, cmd):
        action = cmd[0]
        _cls = cmd[1]
        model_class = getattr(models, _cls)
        slug = cmd[2]

        # get data for this item
        doc_dict = self.uc_dat[_cls.lower()][slug]

        # if a count value, use it to repeat else 1
        cmd_count = cmd[3] if len(cmd)>3 else 1
        for i in range(cmd_count):
            if action == 'add':
                doc = model_class(**doc_dict)
                doc.save()
                assert doc.id
                cmd.append({'doc':doc})
                return [cmd]