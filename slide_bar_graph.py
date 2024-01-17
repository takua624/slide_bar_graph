import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.font_manager as fontm

font_huge = fontm.FontProperties(family="Consolas",size=50)

def HSL_to_RGB(H,S,L):
	# H: 0~360
	# S: 0~1
	# L: 0~1
	if not (0<=H<360 and 0<=S<=1 and 0<=L<=1):
		print("Please make sure that 0<=H<360 and 0<=S<=1 and 0<=V<=1")
		print("return black")
		return (0,0,0)
	C = (1 - np.abs(2*L-1)) * S
	X = C * (1 - np.abs((H/60)%2-1))
	m = L - C/2
	R = m + C*(0<=H<60 or 300<=H<360) + X*(60<=H<120 or 240<=H<300)
	G = m + C*(60<=H<120 or 120<=H<180) + X*(0<=H<60 or 180<=H<240)
	B = m + C*(180<=H<240 or 240<=H<300) + X*(120<+H<180 or 300<=H<360)
	hex_string = "#" + hex(int(R*255))[2:].zfill(2) + hex(int(G*255))[2:].zfill(2) + hex(int(B*255))[2:].zfill(2)
	return (R,G,B, hex_string)

def slide_bar_graph(df, ticklabels=None, colors=None, pale_colors=None, min_max=1, LR_reverse=False, figsize=(22,10), file_name="tmp.png"):
	# df: each column will be plotted as a horizontal bar
	#     for all columns in df, the theoretical max and min values should be the same.
	#     for example, correlation values or lateralization index, whose boundaries are [-1, 1]
	# ticklabels: if None, the column names of "df" will be used
	# colors: the colors for the scattered dots
	# pale_colors: the colors for the background of the dots
	# min_max: the absolute value of the theoretical min and max values. 
	#          I assume this function is used to plot correlation coefficients 
	#          or lateralization indexes, so the default is 1, meaning the theoretical min is -1,
	#          and the theoretical max is 1. Yes, the figure is meant to be symmetrical.
	# LR_reverse: by convention in our lab, lateralization index is positive for left-lateralization.
	#             for visualization, I add this parameter to invert the signs. 
	#             but of course, you can invert the signs of "df" before assigning it to this function.
	# figsize: width x height of the figure
	# file_name: the file name you'd like to save the figure as
	
	cols = df.columns
	n_bars = len(cols)
	if ticklabels==None or n_bars>len(ticklabels):
		ticklabels = df.columns
	if LR_reverse:
		df = -df[cols]
		
	if colors==None:
		colors = ["#c7af49","#9dc3e6","#d6a9db","#99b65a","#bfbfbf"]
	if pale_colors==None:
		pale_colors = ["#fbf6e3","#ebf3fb","#f8e7fa","#f3fce0","#f2f2f2"]
	
	
	if n_bars>len(colors):
		lack = n_bars-len(colors)
		print("Warning: There are %d columns in the data, but only %d colors are specified. The function will randomly generate %d color%s, which are not guaranteed to look nice. You may specify the colors of your choice and run this function again."%(n_bars, len(colors), lack, "s"*(lack>1)))
		# random.seed(0)
		for new_c in range(lack):
			rand_H = random.randint(0,359)
			rand_S = random.random()
			rand_L = 0.2+random.random()*0.4 # we don't want it to be too bright nor too dark
			colors += [HSL_to_RGB(rand_H,rand_S,rand_L)[3]]
			pale_colors += [HSL_to_RGB(rand_H,rand_S,0.92)[3]]
		
	
	fig, ax = plt.subplots(1,1,figsize=figsize)
	
	for ii in range(len(cols)):
		
		ax.plot((-1,1),(n_bars-ii, n_bars-ii),color=pale_colors[ii], zorder=0, linewidth=40)
		ax.scatter(df[cols[ii]], [n_bars-ii]*len(df[cols[ii]]), color=colors[ii], s=100, zorder=1)
		ax.scatter(df[cols[ii]].mean(), n_bars-ii, color="#ffffff", linewidth=3, edgecolors=colors[ii], s=2500, zorder=1)
		ax.scatter(df[cols[ii]].mean(), n_bars-ii, color=colors[ii], s=800, zorder=2)
		ax.text(df[cols[ii]].mean(), n_bars+0.27-ii, "%.2f"%(np.abs(df[cols[ii]].mean())), color=colors[ii], ha="center",fontproperties=font_huge, zorder=0)
	
	plt.ylim([0.6,n_bars+0.6])
	ax.set_yticks(list(range(1,n_bars+1))[::-1])
	ax.set_yticklabels(ticklabels, fontproperties=font_huge)
	xtick_pos = [-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1]
	ax.set_xticks(xtick_pos)
	# ax.set_xticklabels(["1\nLeft", "0.75", "0.5", "0.25", "0", "0.25", "0.5", "0.75", "1\nRight"],fontproperties=font_huge)
	ax.set_xticklabels(["%.2f"%ii*min_max for ii in xtick_pos],fontproperties=font_huge)
	ax.spines["top"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.spines["left"].set_visible(False)
	ax.axvline(0,color="#999999",linestyle="-", linewidth=5, zorder=-1)
	plt.tight_layout()
	plt.savefig(file_name)
	plt.show()
	plt.close()
	
	return
	
df = pd.read_csv("example_data.csv")
ticklabels = ["Code","Lang.","Math","Logic","MSIT","none","what"]
min_max = 1
LR_reverse = True
figsize=(22,10)
file_name="tmp.png"

slide_bar_graph(df=df, ticklabels=ticklabels, min_max=min_max, LR_reverse=LR_reverse, figsize=figsize, file_name=file_name)

