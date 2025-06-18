import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt

#############################
# plots
#############################

def ticks_positions(n: int)->list[int]:
    """Compute ticks position for group of 6 box plots 

    Args:
        - n: total number of box plots

    Returns:
        positions of the grouped ticks labels in the graph
    """
    res = []
    i, c= 1, 0
    while c < n:
        res.append(i)
        c += 1
        if c % 6 == 0: i += 2
        else: i += 1
    return res


def box_plot_show(x: list[list[float]], options: list[str], 
                  colors: list[tuple[float, float, float, float]], form):
    """Display metric box plots of selected populations for one performer and one metric

    Args:
        - x: lists of metrics values for each selected filter
        - options: selected filtered name
        - colors: list of colors (RGBA tuples)
        - form: streamlit form
    """
    fig, axs = plt.subplots(figsize=(9, 4))
    tick_labels=options
    positions=range(len(options))  
    bplot = plt.boxplot(x, tick_labels=tick_labels,
                            positions=positions,
                           showmeans=True, 
                           showfliers=False,  
                           patch_artist=True,
                           medianprops = dict(color = "blue", linewidth = 1.5),
                           meanprops={"marker": "+","markeredgecolor": "black", "markersize": "5"},
                        )
    for i in range(len(bplot['boxes'])):
        bplot['boxes'][i].set(facecolor = colors[i%len(colors)], linewidth=2)
    # Add label for a group of 6 ticks
    axs.tick_params(axis='x', labelsize=12)
    plt.axhline(y=0, color='gray', linestyle='--')
    
    form.pyplot(plt.gcf())

##############################
# stats in dataframe
##############################

def  display_tab(tab: dict[str:dict[str:list]], metric: str='deltaonset'):
    """Display dataframe of statistics for all groups

    Args:
        - tab: {key : [n_elements, mean, q1, q2, q3, mini, maxi, stdev]} from resultat_tot_stats function
        - metric: metric name. Defaults to 'deltaonset'.
    """
    precision=4
    st.header(f"metric: {metric}")
    tab_results = pd.DataFrame.from_dict(tab)
    
    keys = list(tab.keys())
    #st.write(keys)
    res=""
    for k in keys:
        s = str(round(tab[k][1]*100,2)) + " ± " + str(round(tab[k][7]*100,2)) + " & "
        res+= s
    #st.write(res)    
        
    
    tab_results.iloc[0] = tab_results.iloc[0].round(0)  # integers for the first line (N _elements)
    tab_results.iloc[1:] = tab_results.iloc[1:].round(precision)
    tab_results.index=['N_elements', 'mean', 'q1', 'median', 'q3', 'mini', 'maxi', 'stddev']
    
    labove, rabove = 0.01, 0.1
    lbelow, rbelow = (-0.01, -0.1) # pb negative number for highlight
    
    st.dataframe(tab_results.style.format(lambda x: "{:.0f}".format(x) if x == round(x) else "{:.4f}".format(x))
                                    .highlight_between(subset=(slice("median","median"), tab_results.columns),
                                                       left=labove, right=rabove, color="lightgreen")
                                    .highlight_between(subset=(slice("median","median"), tab_results.columns),
                                                       left=lbelow, right=rbelow, color="lightpink"))