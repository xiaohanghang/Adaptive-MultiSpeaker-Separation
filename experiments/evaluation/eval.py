# coding: utf-8
from utils.trainer import *
from models.L41 import L41Model
from utils.bss_eval import bss_eval_sources, bss_eval_sources_cupy
import numpy as np
from models.dpcl import DPCL

if __name__ == '__main__':
	p = MyArgs()

	p.parser.add_argument('--model_folder', help='Path to the Model folder to load', required=True) 
	p.parser.add_argument('--sortofmodel', help='Sort of model', required=True) 
	p.add_adapt_args()
	p.add_separator_args()
	args = p.get_args()

	if 'STFT' in args.sortofmodel:
		if 'enhanced' in args.sortofmodel:
			inferencer = STFT_Separator_Enhanced_Inference
		else:
			inferencer = STFT_Separator_Inference
	elif 'front' in args.sortofmodel:
		if 'enhanced' in args.sortofmodel:
			inferencer = Front_Separator_Enhanced_Inference
		else:
			inferencer = Front_Separator_Inference
	elif 'pretraining' in args.sortofmodel:
		inferencer = Pretrained_Inference
	else:
		exit()
	
	if 'L41' in args.sortofmodel:
		sep = L41Model	
	elif 'DPCL' in args.sortofmodel:
		sep = DPCL
	else:
		sep = None

	inferencer = inferencer(sep, 'inference', **vars(args))

	sdr = 0.0
	sir = 0.0
	sar = 0.0
	i = 0
	for mix, non_mix, separated in inferencer.inference():
		for m, n_m, s in zip(list(mix), list(non_mix), list(separated)):
			mix_stack = np.array([m, m])
			
			no_separation = bss_eval_sources_cupy(n_m, mix_stack)
			separation = bss_eval_sources_cupy(n_m, s)

			sdr_ = np.mean(separation[0] - no_separation[0])
			sir_ = np.mean(separation[1] - no_separation[1])
			sar_ = np.mean(separation[2] - no_separation[2])

			sdr += sdr_
			sir += sir_
			sar += sar_
			
			i += 1

			print sdr/float(i), sir/float(i), sar/float(i)