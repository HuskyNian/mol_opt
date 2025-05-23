from __future__ import print_function

import argparse
import yaml
import os
import sys
sys.path.append(os.path.realpath(__file__))
from tdc import Oracle
from time import time 
import numpy as np 

''' 
name "qed:1+jnk:2"
python run.py graph_ga --oracles qed:1+jnk3:1+drd2:1+gsk3b:1+sa:1
'''
class MultiOracle(Oracle): 

    def __init__(self, name, target_smiles=None, num_max_call=None, **kwargs):
        name_split = name.split('+')
        self.name_list = [i.split(':')[0] for i in name_split] # ['qed', 'jnk3', 'drd2', 'gsk3b', 'sa']
        self.weight_list = [float(i.split(':')[1]) for i in name_split] 
        self.weight_list = [i/sum(self.weight_list) for i in self.weight_list] 
        self.oracle_list = [Oracle(i, target_smiles, num_max_call, **kwargs)\
                             for i in self.name_list]  
        self.name = name 

    #def __call__(self, *args, **kwargs):
    #    return np.sum([oracle(*args, **kwargs)*weight for oracle,weight in zip(self.oracle_list, self.weight_list)])

    def __call__(self, *args, **kwargs):
        total = 0
        for i,p in enumerate(self.name_list):
            if p in ['qed','jnk3','bbbp1']:
                total += self.oracle_list[i](*args,**kwargs)
            elif p == 'sa':
                total += 1- (self.oracle_list[i](*args,**kwargs) -1 ) /9
            elif p in ['gsk3b','drd2','smarts_filter']:
                total += 1-self.oracle_list[i](*args,**kwargs)
            elif p in ['logs']:
                total += (self.oracle_list[i](*args,**kwargs) + 8 ) / (9)
            elif p in ['reduction_potential']:
                total += 1-  abs( np.clip(self.oracle_list[i](*args,**kwargs),-2.3,-0.3) +1.3)
            else:
                raise NotImplementedError("{p} property is not defined in base.py")
        return total



def main():
    start_time = time() 
    parser = argparse.ArgumentParser()
    parser.add_argument('method', default='graph_ga')
    parser.add_argument('--smi_file', default=None)
    parser.add_argument('--config_default', default='hparams_default.yaml')
    parser.add_argument('--config_tune', default='hparams_tune.yaml')
    parser.add_argument('--pickle_directory', help='Directory containing pickle files with the distribution statistics', default=None)
    parser.add_argument('--n_jobs', type=int, default=-1)
    parser.add_argument('--output_dir', type=str, default=None)
    parser.add_argument('--patience', type=int, default=5)
    parser.add_argument('--max_oracle_calls', type=int, default=5000)
    parser.add_argument('--freq_log', type=int, default=100)
    parser.add_argument('--n_runs', type=int, default=5)
    # parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--seed', type=int, nargs="+", default=[42,43,44,45,46])
    parser.add_argument('--task', type=str, default="simple", choices=["tune", "simple", "production"])
    parser.add_argument('--oracles', nargs="+", default=["QED"]) ### 
    parser.add_argument('--log_results', action='store_true')
    parser.add_argument('--log_code', action='store_true')
    parser.add_argument('--init_method', type=str,default="random1",choices=['random1','best100','worst100'])
    parser.add_argument('--wandb', type=str, default="disabled", choices=["online", "offline", "disabled"])
    args = parser.parse_args()

    os.environ["WANDB_MODE"] = args.wandb

    if not args.log_code:
        os.environ["WANDB_DISABLE_CODE"] = "false"

    args.method = args.method.lower() 

    path_main = os.path.dirname(os.path.realpath(__file__))
    path_main = os.path.join(path_main, "main", args.method)

    sys.path.append(path_main)
    
    print(args.method)
    # Add method name here when adding new ones
    if args.method == 'screening':
        from main.screening.run import Exhaustive_Optimizer as Optimizer 
    elif args.method == 'molpal':
        from main.molpal.run import MolPAL_Optimizer as Optimizer
    elif args.method == 'graph_ga':
        from main.graph_ga.run import GB_GA_Optimizer as Optimizer
    elif args.method == 'smiles_ga':
        from main.smiles_ga.run import SMILES_GA_Optimizer as Optimizer
    elif args.method == "selfies_ga":
        from main.selfies_ga.run import SELFIES_GA_Optimizer as Optimizer
    elif args.method == "synnet":
        from main.synnet.run import SynNet_Optimizer as Optimizer
    elif args.method == 'hebo':
        from main.hebo.run import HEBO_Optimizer as Optimizer 
    elif args.method == 'graph_mcts':
        from main.graph_mcts.run import Graph_MCTS_Optimizer as Optimizer
    elif args.method == 'smiles_ahc':
        from main.smiles_ahc.run import AHC_Optimizer as Optimizer
    elif args.method == 'smiles_aug_mem':
        from main.smiles_aug_mem.run import AugmentedMemory_Optimizer as Optimizer 
    elif args.method == 'smiles_bar':
        from main.smiles_bar.run import BAR_Optimizer as Optimizer 
    elif args.method == "smiles_lstm_hc":
        from main.smiles_lstm_hc.run import SMILES_LSTM_HC_Optimizer as Optimizer
    elif args.method == 'selfies_lstm_hc':
        from main.selfies_lstm_hc.run import SELFIES_LSTM_HC_Optimizer as Optimizer
    elif args.method == 'dog_gen':
        from main.dog_gen.run import DoG_Gen_Optimizer as Optimizer
    elif args.method == 'gegl':
        from main.gegl.run import GEGL_Optimizer as Optimizer 
    elif args.method == 'boss':
        from main.boss.run import BOSS_Optimizer as Optimizer
    elif args.method == 'chembo':
        from main.chembo.run import ChemBOoptimizer as Optimizer 
    elif args.method == 'gpbo':
        from main.gpbo.run import GPBO_Optimizer as Optimizer
    elif args.method == 'stoned': 
        from main.stoned.run import Stoned_Optimizer as Optimizer
    elif args.method == "selfies_vae":
        from main.selfies_vae.run import SELFIES_VAEBO_Optimizer as Optimizer
    elif args.method == "smiles_vae":
        from main.smiles_vae.run import SMILES_VAEBO_Optimizer as Optimizer
    elif args.method == 'jt_vae':
        from main.jt_vae.run import JTVAE_BO_Optimizer as Optimizer
    elif args.method == 'dog_ae':
        from main.dog_ae.run import DoG_AE_Optimizer as Optimizer
    elif args.method == 'pasithea':
        from main.pasithea.run import Pasithea_Optimizer as Optimizer
    elif args.method == 'dst':
        from main.dst.run import DST_Optimizer as Optimizer        
    elif args.method == 'molgan':
        from main.molgan.run import MolGAN_Optimizer as Optimizer
    elif args.method == 'mars':
        from main.mars.run import MARS_Optimizer as Optimizer
    elif args.method == 'mimosa':
        from main.mimosa.run import MIMOSA_Optimizer as Optimizer
    elif args.method == 'gflownet':
        from main.gflownet.run import GFlowNet_Optimizer as Optimizer
    elif args.method == 'gflownet_al':
        from main.gflownet_al.run import GFlowNet_AL_Optimizer as Optimizer
    elif args.method == 'moldqn':
        from main.moldqn.run import MolDQN_Optimizer as Optimizer
    elif args.method == 'reinvent':
        from main.reinvent.run import REINVENT_Optimizer as Optimizer
    elif args.method == 'reinvent_selfies':
        from main.reinvent_selfies.run import REINVENT_SELFIES_Optimizer as Optimizer
    elif args.method == 'graphinvent':
        from main.graphinvent.run import GraphInvent_Optimizer as Optimizer
    elif args.method == "rationale_rl":
        from main.rationale_rl.run import Rationale_RL_Optimizer as Optimizer
    else:
        raise ValueError("Unrecognized method name.")


    if args.output_dir is None:
        args.output_dir = os.path.join(path_main, "results")
    
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    if args.pickle_directory is None:
        args.pickle_directory = path_main

    if args.task != "tune":
    
        for oracle_name in args.oracles:

            print(f'Optimizing oracle function: {oracle_name}')

            try:
                config_default = yaml.safe_load(open(args.config_default))
            except:
                config_default = yaml.safe_load(open(os.path.join(path_main, args.config_default)))

            oracle = MultiOracle(name = oracle_name)
            optimizer = Optimizer(args=args)

            if args.task == "simple":
                # optimizer.optimize(oracle=oracle, config=config_default, seed=args.seed) 
                for seed in args.seed:
                    print('seed', seed)
                    optimizer.optimize(oracle=oracle, config=config_default, seed=seed)
            elif args.task == "production":
                optimizer.production(oracle=oracle, config=config_default, num_runs=args.n_runs)
            else:
                raise ValueError('Unrecognized task name, task should be in one of simple, tune and production.')

    elif args.task == "tune":

        print(f'Tuning hyper-parameters on tasks: {args.oracles}')

        try:
            config_default = yaml.safe_load(open(args.config_default))
        except:
            config_default = yaml.safe_load(open(os.path.join(path_main, args.config_default)))

        try:
            config_tune = yaml.safe_load(open(args.config_tune))
        except:
            config_tune = yaml.safe_load(open(os.path.join(path_main, args.config_tune)))

        oracles = [MultiOracle(name = oracle_name) for oracle_name in args.oracles]
        optimizer = Optimizer(args=args)
        
        optimizer.hparam_tune(oracles=oracles, hparam_space=config_tune, hparam_default=config_default, count=args.n_runs)

    else:
        raise ValueError('Unrecognized task name, task should be in one of simple, tune and production.')
    end_time = time()
    hours = (end_time - start_time) / 3600.0
    print('---- The whole process takes %.2f hours ----' % (hours))
    # print('If the program does not exit, press control+c.')


if __name__ == "__main__":
    main()

