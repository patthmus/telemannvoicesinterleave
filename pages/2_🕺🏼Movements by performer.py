# -*- coding: utf-8 -*-
"""
This module defines the streamlit application movements page
"""

import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from src.durations_analyse_tools import *
from src.data import *
from src.stats import *
from src.streamlit_displays import *

#############################
# PAGE CONFIG
#############################

def config_page():
    st.set_page_config(layout="wide", 
                       page_title="Analyse by type of Movement", 
                       page_icon="🕺🏼")


##############################
# main function
##############################
    
def by_movements(): 
    st.header("Analyse by type of Movement and by performer on all the corpus")
    # call back to update options for box plot
    def pill_callback():
        for key in st.session_state.keys():
            del st.session_state[key]
            
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    
    with st.container(border=True):
        names = [p for p in PERFORMERS]
        performer= st.pills("choose a performer", 
                            names, 
                            default='kuijken', 
                            on_change=pill_callback)
        
        metric= st.pills("choose a metric", 
                         ['deltaonset', 'deltaioi'], 
                         default='deltaioi', 
                         on_change=pill_callback)
        
        movement_name=st.selectbox("choose a type of movement", 
                                   MOVEMENTS_POSITIONS.keys(), 
                                   on_change=pill_callback)
    
    if 'performers_metric_results' not in st.session_state:
        metric_all, data_all = get_all_metric_and_data_for_one_performer(performer, metric=metric, movement_name= movement_name)
        ####### dataframe with raw data and ioi_ratios ######################
        dfdata = pd.DataFrame.from_dict(data_all)
        dfdata[metric]=metric_all
        st.session_state.dfdata=dfdata
        ######################################################################
    # display stats
        performers_metric_results=timings(metric, performer, metric_all, data_all)
        st.session_state.performers_metric_results = performers_metric_results
        statistics= results_to_stats(st.session_state.performers_metric_results[performer])
        st.session_state.statistics = statistics
    
    for f in MOVEMENTS_POSITIONS[movement_name]:
        st.write(f"Fantasia {f} -- movement(s) n°: {'-'.join([str(n) for n in MOVEMENTS_POSITIONS[movement_name][f]])}")
        
    N=len(st.session_state.statistics)
    display_tab(st.session_state.statistics, metric=metric)
    
    with st.expander("See data"):
        st.session_state.dfdata
        
    form_fantasia = st.form("form_fantasia")
    with form_fantasia:
        options=st.multiselect(
            "Select filters:",
            list(st.session_state.statistics.keys())
        )
        submitted = form_fantasia.form_submit_button("Display Box plot")
        if submitted:
            x= [st.session_state.performers_metric_results[performer][k] for k in options]
            cmap = plt.get_cmap('tab20c')
            colors = [cmap(i / (N-1)) for i in range(N)]
            box_plot_show(x, options, colors, form_fantasia)


##############################
# on load
##############################

config_page()
by_movements()