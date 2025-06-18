# -*- coding: utf-8 -*-
"""
This module defines the streamlit application corpus by performer page
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
                       page_title="Analyse for the entire corpus", 
                       page_icon="🪈")


#############################
# plots
#############################

def plot_times_fantasias(dicts_perf: dict[str:dict[int:float]]):
    """Display fantasias durations across performers

    Args:
        - dicts_perf: dictionnary keys : performer name
                                  value : dictionnary with keys fantasia number 
                                                           and value time_duration
    """
    x = list(range(1,13))
    # plots durations comparisons
    kuijken = list(dicts_perf['kuijken'].values())
    rampal = list(dicts_perf['rampal'].values())
    pitelina = list(dicts_perf['pitelina'].values())
    lazarevitch = list(dicts_perf['lazarevitch'].values())
    pahud = list(dicts_perf['pahud'].values())
    porter = list(dicts_perf['porter'].values())
    fig, ax = plt.subplots(figsize=(20,10))
    ax.plot(x, kuijken, label='kuijken')
    ax.plot(x, rampal, label='rampal')
    ax.plot(x, pitelina, label='pitelina')
    ax.plot(x, lazarevitch, label='lazarevitch')
    ax.plot(x, pahud, label='pahud')
    ax.plot(x, porter, label='porter')
    ax.set_title("Duration by fantasia and by performer")
    st.pyplot(plt.gcf())


##############################
# main function
##############################
    
def fantasias_performers():
    tab_f1, tab_f2 = st.tabs(["Durations", "Results"])
    with tab_f1:
        dicts_perf=fantasias_durations_in_all_perf()
        tab = pd.DataFrame(fantasias_durations_in_all_perf(), index=[i for i in range(1,13)])
        col1, col2 = st.columns(2, gap="small", border = True)
        col1.subheader("Durations for all the fantasias (ms)")
        with col1:
            tab
        with col2:
            plot_times_fantasias(dicts_perf)
            
    with tab_f2:   
        st.header("Analyse by performer for all the corpus")
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
                             default='deltaonset', 
                             on_change=pill_callback)
        
        if 'performers_metric_results' not in st.session_state:
            metric_all, data_all = get_all_metric_and_data_for_one_performer(performer, metric=metric)
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
            
        st.divider()
        N=len(st.session_state.statistics)
        display_tab(st.session_state.statistics, metric=metric)
        
        st.divider()
        with st.expander("See data"):
            st.session_state.dfdata
        
        st.divider()   
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
fantasias_performers()