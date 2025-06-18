# -*- coding: utf-8 -*-
"""
This module defines the streamlit application measures page
"""

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
from matplotlib import pyplot as plt
from src.durations_analyse_tools import *
from src.data import *
from src.stats import *
from src.streamlit_displays import display_tab


#############################
# PAGE CONFIG
#############################

def config_page():
    st.set_page_config(layout="wide", 
                       page_title="Analyse by measure", 
                       page_icon="🎼")


#############################
# score
#############################

def display_score(fantasia: int):
    """Display score pdf
    
    Args:
        - fantasia: fantasia number
    """
    
    with st.container():
        pdf_viewer(f"{PDFS}/Fantasia{fantasia}.pdf")

#############################
# videos
#############################
def get_video_boundaries(fantasia_data: list[dict], 
                         start: int, end: int, repeated: int)->tuple[int, int]:
    """Returns time boundaries of selected excerpt

    Args:
        - fantasia_data: data of selected fantasia
        - start: start bar 
        - end: end bar
        - repeated: bar occurence

    Returns:
        - start and end times of youtube video in seconds
    """
    i=0
    while fantasia_data[i]["measure"]!= str(start) or fantasia_data[i]["repeated"]!=str(repeated):
        i+=1
    video_start = float(fantasia_data[i]["onset"])/1000
    while fantasia_data[i]["measure"]!= str(end) or fantasia_data[i]["repeated"]!=str(repeated):
        i+=1
    while fantasia_data[i]["measure"]==str(end):
        i+=1
    video_end = float(fantasia_data[i]["onset"])/1000 +1
    return video_start, video_end

#############################
# plots
#############################

def display_plot(data: list , metric_data: list , 
                 median_global: float , median_upper_voice: float , median_lower_voice: float , 
                 metric: str='deltaonset'):
    """Display metric values graph for selected bars with voices annotations

    Args:
        - data: data of selected bars
        - metric_data: computed metric for each element of data
        - median_global: metric values median
        - median_upper_voice: metric values median for filtered upper voice data
        - median_lower_voice: metric values median for filtered lower voice data
        - metric: selected metric (deltaonset or deltaioi). Defaults to 'deltaonset'.
    """
    voices= [e['voice'] for e in data]
    xs=get_positions_in_measures_fractions(data)
    xlabel = 'measure n°'
    width=0.05
    
    fig, ax = plt.subplots(figsize=(20,10))
    colors = ["red" if e=='u' else "blue" if e in 'bBst' else 'green' if e =='m' else 'grey' for e in voices]
    hatches= [".." if e=='.' else None for e in voices]
    ax.bar(xs, metric_data, width=width, color=colors, hatch=hatches)# legend rest, voice
    for x,y, voice in zip(xs, metric_data, voices):
        if voice in 'Bst':
            label = 'B'
        elif voice=='u':
            label='u'
        elif voice=='m':
            label='m'
        elif voice=='b':
            label='b'
        else:
            label = voice
        
        if label not in 'x.':
            ax.annotate(label, # this is the text
                        (x,y), # these are the coordinates to position the label
                        textcoords="offset points", # how to position the text
                        xytext=(0,10), # distance from text to points (x,y)
                        ha='center') # horizontal alignment can be left, right or center

    ax.plot(xs, [median_global for _ in range(len(xs))], 
            color="black", label='median for all notes')
    ax.plot(xs, [median_upper_voice for _ in range(len(xs))],
            color ="red", label='median for upper voice notes')
    ax.plot(xs, [median_lower_voice for _ in range(len(xs))], 
            color="blue", label='median for lower voice notes')
    ax.plot(xs, [0.0  for _ in range(len(xs))], 
            linestyle='dashed', color="black")
    plt.xlabel(xlabel)
    plt.ylabel(metric)
    ax.legend()
    st.pyplot(plt.gcf())    


##############################
# main function
##############################

def  by_measures():
    st.header("Analyse on selected measures by performer")
    tab_m1, tab_m2 = st.tabs(["Selected measures", "Results"])
    with tab_m1:
        # columns layout    
        col1, col2 = st.columns(2, gap="large")
        col1.subheader("inputs")
        col2.subheader("score")
        
        def pill_callback():
            for key in st.session_state.keys():
                del st.session_state[key]
                
        with col1:
            fantasia = st.number_input("choose a fantasia", min_value=1, max_value=12, step=1, 
                                    on_change=pill_callback)
            
            start = st.number_input("choose a starting measure", min_value=1, step=1, 
                                    on_change=pill_callback)
            
            end = st.number_input("choose an ending measure", 
                                min_value=1, step=1, value=2, 
                                on_change=pill_callback)
            
            repeated = st.number_input("choose a repeat if exists (0 if not)", 
                                min_value=0, max_value=3, step=1, value=0, 
                                on_change=pill_callback)
            
            performer= st.pills("choose a performer", 
                                [p for p in PERFORMERS], default="kuijken", 
                                on_change=pill_callback)
            
            metric= st.pills("choose a metric", ['deltaonset', 'deltaioi'], 
                            default='deltaonset', 
                            on_change=pill_callback)

        with col2:
            display_score(fantasia)
                
    with tab_m2:
        # columns layout    
        col3, col4 = st.columns(2, gap="large")
        col3.subheader("video")
        col4.subheader("plots")
 
        if 'performers_metric_measure_results' not in st.session_state:
            fantasia_data_measure = get_all_data(performer, fantasia)
            try:
                video_start, video_end = get_video_boundaries(fantasia_data_measure, start, end, repeated)
                video_url = f"https://www.youtube.com/watch?v={YT_ID[performer][fantasia]}"

                with col3:
                    st.video(video_url, start_time=video_start, end_time=video_end)
                    st.warning(f"if embeded video doesn't load, watch directly on youtube __start time: {round(video_start)}s, end: {round(video_end)}s__")

                data_measures = [m for m in fantasia_data_measure 
                                if (m['measure']!= 'x' 
                                    and int(m['measure'])>=start 
                                    and int(m['measure'])<=end)
                                    and (int(m['repeated']))==repeated] 
                          
                data_all, monsets_all, real_onsets_all, metric_all =[], [], [], []
                for m in range(start, end+1):
                    datafiltered= [d for d in data_measures if int(d['measure'])== m]
                    data_all.extend(datafiltered)
                    #real iois based on the onset in ms
                    iois=[float(m['ioi']) for m in datafiltered]
                    #get predicted metronomic time durations for all notes
                    metronomic_ioi= get_metronomic_ioi(datafiltered)
                    real_onsets = [float(m['onset']) for m in datafiltered]
                    real_onsets_all.extend(real_onsets)

                    metronomic_onsets = []
                    acc=real_onsets[0]
                    metronomic_onsets.append(acc)
                    for i in range(1, len(real_onsets)):
                        acc += metronomic_ioi[i-1]
                        metronomic_onsets.append(acc)
                    monsets_all.extend(metronomic_onsets)

                    if metric == "deltaioi":
                        metric_all.extend(get_delta_ioi_per_measure(iois, metronomic_ioi))
                    elif metric == "deltaonset":
                        metric_all.extend(get_delta_onset_per_measure(real_onsets, metronomic_onsets, iois))
                        
                ####### dataframe with raw data and computed metric ######################
                dfdata = pd.DataFrame.from_dict(data_all)
                dfdata[metric]=metric_all
                st.session_state.dfdata_measure=dfdata
                ######################################################################
                
                performers_results=timings(metric, performer, metric_all, data_all )
                results = results_to_stats(performers_results[performer])
                ### paper notations
                median_global, median_upper_voice, median_lower_voice  = results['all'][1], results['u'][1], results['B+b'][1]

                # display stats
                performers_metric_measure_results=timings(metric, performer, metric_all, data_all)
                st.session_state.performers_metric_measure_results = performers_metric_measure_results
                statistics= results_to_stats(st.session_state.performers_metric_measure_results[performer])
                st.session_state.statistics_measure = statistics
                st.divider()
                st.write("Analyse on only the first sequence of notes if measures are repeated")
                N=len(st.session_state.statistics_measure)
                display_tab(st.session_state.statistics_measure, metric=metric)
                with st.expander("See data on selected measures"):
                    st.session_state.dfdata_measure
                with col4:
                    display_plot(data_all, metric_all, median_global, median_upper_voice, median_lower_voice, metric=metric)
            except:
                st.warning("Invalid boundaries in measures or an incorrect repeat", icon="⚠️")
                st.warning("Please check the inputs", icon="🙏")
                
##############################
# on load
##############################

config_page()
by_measures()