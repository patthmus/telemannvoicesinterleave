# -*- coding: utf-8 -*-
"""
This module defines the streamlit application fugatos page
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
                       page_title="Analyse for fugatos movements", 
                       page_icon="🎶")


##############################
# main function
##############################

def fugatos_performers():
    st.header("Analyse by performer for all fugatos movements")
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
                            names, default='kuijken', on_change=pill_callback)
        
        metric= st.pills("choose a metric", 
                         [ 'deltaonset', 'deltaioi'], 
                         default='deltaonset', 
                         on_change=pill_callback)
    
    if 'performers_fugatos' not in st.session_state:
        metric_all, data_all = get_all_metric_and_data_for_one_performer(performer, metric=metric, fugato=True)
        ####### dataframe with raw data and ioi_ratios ######################
        dfdata = pd.DataFrame.from_dict(data_all)
        dfdata[metric]=metric_all
        st.session_state.dfdata=dfdata
        ######################################################################
    # display stats
        performers_fugatos=timings(metric, performer, metric_all, data_all)
        st.session_state.performers_fugatos = performers_fugatos

        stats_fugatos= results_to_stats(st.session_state.performers_fugatos[performer])
        st.session_state.stats_fugatos = stats_fugatos
    
    N=len(st.session_state.stats_fugatos)
    display_tab(st.session_state.stats_fugatos, metric=metric)
    
    with st.expander("See data"):
        st.session_state.dfdata
        
    form_one = st.form("form_one")
    with form_one:
        options=st.multiselect(
            "Select filters:",
            list(st.session_state.stats_fugatos.keys())
        )
        submitted = form_one.form_submit_button("Display Box plot")
        if submitted:
            x= [st.session_state.performers_fugatos[performer][k] for k in options]
            cmap = plt.get_cmap('tab20c')
            colors = [cmap(i / (N-1)) for i in range(N)]
            box_plot_show(x, options, colors, form_one)


##############################
# on load
##############################

config_page()
fugatos_performers()