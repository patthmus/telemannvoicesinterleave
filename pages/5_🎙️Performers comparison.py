# -*- coding: utf-8 -*-
"""
This module defines the streamlit application performers comparison page
"""

import streamlit as st
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from src.durations_analyse_tools import *
from src.data import *
from src.stats import *
from src.streamlit_displays import ticks_positions

#############################
# PAGE CONFIG
#############################

def config_page():
    st.set_page_config(layout="wide", 
                       page_title="Comparison beetween performers on the entire corpus", 
                       page_icon="🎙️")

config_page()


#############################
# multi boxplots
#############################


def box_plot_show(x, options, colors, form, metric='deltatioi'):

    fig, axs = plt.subplots(figsize=(20,10))
    n_labels=len(colors)*len(options)
    tick_labels=n_labels*[' ']
    positions=ticks_positions(len(x))
    bplot = plt.boxplot(x, tick_labels=tick_labels,
                            positions=positions,
                           showmeans=True, 
                           showfliers=False,  
                           patch_artist=True,
                           medianprops = dict(color = "blue", linewidth = 1.5),
                           meanprops={"marker": "+",
                                      "markeredgecolor": "black", 
                                      "markersize": "5"},
                        )
    for i in range(len(bplot['boxes'])):
        bplot['boxes'][i].set(facecolor = colors[i%len(colors)], linewidth=2)
    # Add label for a group of 6 ticks
    axs.tick_params(axis = 'x', length = 0)
    i=0
    for k in options:
        pos = 3.5 + i
        axs.text(pos, -0.02, k, ha='center',
                    va='top', transform=axs.get_xaxis_transform(), fontsize=25)
        i+=7
    custom_lines = [Line2D([0], [0], color=colors[i], lw=4) for i in range(len(colors))]
    axs.legend(custom_lines, [p[0].upper()+p[1:] for p in PERFORMERS], 
                fontsize=21, ncols=6)
    
    if metric == 'deltaonset' :
        plt.axhline(y=0, color='gray', linestyle='--')
        ylabel="$\Delta \mathit{o}(\%)$"
    elif metric =='deltaioi' :
        plt.axhline(y=0, color='gray', linestyle='--')
        ylabel="$\Delta \mathit{IOI}(\%)$"   
    
    axs.grid(axis='y', linestyle='--', linewidth=1)
    axs.set_ylabel(ylabel, fontsize=30)
    axs.tick_params(axis='y', labelsize=30) 
    form.pyplot(plt.gcf())



#############################
# main functions
#############################


def performers_global_deltaioi():
    """Boxplots comparing the 6 performers deltas ioi per measure on several features
    """
    st.write("# Box plots  of $\Delta \mathit{IOI}(\%)$ by performers and grouped by selected categories")
    st.write("$\Delta \mathit{IOI} = \dfrac{\mathit{IOI_p}-\mathit{IOI_m}}{dur(M)}$")    
         
    with st.spinner("Wait for it....around 20s", show_time=True):
        if 'all_performers_deltas_ioi' not in st.session_state:
            all_performers_deltas_ioi=timings('deltaioi')
            st.session_state.all_performers_deltas_ioi=all_performers_deltas_ioi
            st.toast('Done!', icon='🎉')
    form_all_deltas_ioi = st.form("form_all_deltas_ioi")
    with form_all_deltas_ioi:# voir session state pour 
        options_deltas_ioi=st.multiselect(
            "Select filters:",
            list(st.session_state.all_performers_deltas_ioi['kuijken'].keys())
        )
        submitted_deltas_ioi = form_all_deltas_ioi.form_submit_button("Display Box plots")
        if submitted_deltas_ioi:    
            cmap = plt.get_cmap('Accent')
            colors = [cmap(i / 7) for i in range(6)]
            x=[]
            for k in options_deltas_ioi:
                x += [[e*100 for e in st.session_state.all_performers_deltas_ioi[p][k]]
                      for p in st.session_state.all_performers_deltas_ioi.keys()]
            fig, ax = plt.subplots(figsize=(9, 4))
            box_plot_show(x, options_deltas_ioi, colors,
                          form_all_deltas_ioi, metric='deltaioi')


def performers_global_deltaonset():
    """Boxplots comparing the 6 performers deltas onset per measure on several features
    """
    st.write("# Box plots  of $\Delta \mathit{o}(\%)$  by performers and grouped by selected categories")
    st.write("$\Delta \mathit{o} = \dfrac{\mathit{o_p}-\mathit{o_m}}{dur(M)}$")    
         
    with st.spinner("Wait for it....around 20s", show_time=True):
        if 'all_performers_deltas_onset' not in st.session_state:
            all_performers_deltas_onset=timings('deltaonset')
            st.session_state.all_performers_deltas_onset=all_performers_deltas_onset
            st.toast('Done!', icon='🎉')
    form_all_deltas_onset = st.form("form_all_deltas_onset")
    with form_all_deltas_onset:# voir session state pour 
        options_deltas_onset=st.multiselect(
            "Select filters:",
            list(st.session_state.all_performers_deltas_onset['kuijken'].keys())
        )
        submitted_deltas_onset = form_all_deltas_onset.form_submit_button("Display Box plots")
        if submitted_deltas_onset:    
            cmap = plt.get_cmap('Accent')
            colors = [cmap(i / 7) for i in range(6)]
            x=[]
            for k in options_deltas_onset:
                x += [[e*100 for e in st.session_state.all_performers_deltas_onset[p][k]]
                      for p in st.session_state.all_performers_deltas_onset.keys()]
            fig, ax = plt.subplots(figsize=(9, 4))
            box_plot_show(x, options_deltas_onset, colors, 
                          form_all_deltas_onset, metric='deltaonset')         
            
            
####################
## layout
####################

page_names_to_funcs = {
    "ΔIOI": performers_global_deltaioi,
    "Δonset": performers_global_deltaonset
}

select = st.sidebar.selectbox("Choose a visualisation", 
                              page_names_to_funcs.keys())
page_names_to_funcs[select]()