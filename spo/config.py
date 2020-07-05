import os

DATA_DIR = os.environ['DATA_DIR']

triggers = ['leads to', 'cause of', 'causes', 'cause', 'inhibit']
s_dp_list = ['nsubj', '_acl:relcl', 'nsubj:pass', '_xcomp']
o_dp_list = ['obj', 'obl', 'nmod']