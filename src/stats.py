from statistics import mean, quantiles, pstdev
from src.durations_analyse_tools import *

#####################################
#ioi
######################################

def get_metric_of_selected_elements(metric_data:list[float], 
                                 data: list[dict[str:str]], 
                                 rest_filtered: bool=False, 
                                 select_voice: str=None, 
                                 d: float=None, 
                                 beats_indexes: list[float]=None)->list:
    """Returns a sequence of selected metric values according to arguments values

    Args:
        - metric_data : sequence of deltaioi or deltaonset
        - data : 
        - rest_filtered: False if rests are take into account, True otherwise. Defaults to False
        - select_voice: voice selected. Defaults to None
        - d : (in quarter note) None if all durations, otherwise filter on a specific duration for only notes (not rest)
             Defaults to None
        - beats_indexes: Indexes of beats. Defaults to None if all elements used

    Returns:
        sequence of metric values
    """
    tab=[]
    ## sequence of indexes depending on beats:
    if beats_indexes==None:
        beats_indexes = range(len(data))
    ## all durations    
    if d==None :
        if rest_filtered:
            tab = [metric_data[i] for i in beats_indexes if data[i]['voice']!='.']
        elif select_voice!=None:
            tab = [metric_data[i] for i in beats_indexes if data[i]['voice'] in select_voice]
        else:
            tab = metric_data
    ## specific duration    
    elif d!=None :
        if rest_filtered:
            tab = [metric_data[i] for i in beats_indexes if (data[i]['duration']==str(d) and data[i]['voice']!='.')]
        elif select_voice!=None:
            tab = [metric_data[i] for i in beats_indexes if (data[i]['duration']==str(d) and data[i]['voice'] in select_voice)]
        else:
            tab = [metric_data[i] for i in beats_indexes if data[i]['duration']==str(d)]      
    return tab


def get_metric_results(metric_data: list[float], datas: list[str])->dict[str:list[float]]:
    """Returns all metric values for all categories used in the web app
    
    Args:
        - metric_data : sequence of deltaioi or deltaonset
        - datas : corresponding data

    Returns:
        {selected group : metric values}
    """
    results=dict()
    # get list of measures positions in float
    measures_positions = get_positions_in_measures_fractions(datas)
    # get indexes of beats (on/off/first)
    on_beats = filtered_beats_indexes(datas, measures_positions, 'on')
    off_beats = filtered_beats_indexes(datas, measures_positions, 'off')
    first_beats = filtered_beats_indexes(datas, measures_positions, 'first')
    
    #for sixteenth notes in position 1,2,3,4 of a group of 4 in binary meter 2/4, 3/4 and 4/4
    sixteenth_p1_indexes= get_binary_sixteenth_indexes(datas, measures_positions, 1)
    sixteenth_p2_indexes= get_binary_sixteenth_indexes(datas, measures_positions, 2)
    sixteenth_p3_indexes= get_binary_sixteenth_indexes(datas, measures_positions, 3)
    sixteenth_p4_indexes= get_binary_sixteenth_indexes(datas, measures_positions, 4)
    
    ###########interleaved sixteenth notes stats or xxxx #############################
    sixteenth_p1_indexes_interleaved=[]
    for i in sixteenth_p1_indexes:
        if datas[i]['voice']+datas[i+1]['voice']+datas[i+2]['voice']+datas[i+3]['voice'] in ['BuBu', 'Bubu', 'uBuB', 'bubu', 'buBu', 'uBuB']:
            sixteenth_p1_indexes_interleaved.append(i)

    ##########################################################################
    sixteenth_p2_indexes_interleaved=[i+1 for i in sixteenth_p1_indexes_interleaved]
    sixteenth_p3_indexes_interleaved=[i+2 for i in sixteenth_p1_indexes_interleaved]
    sixteenth_p4_indexes_interleaved=[i+3 for i in sixteenth_p1_indexes_interleaved]
    
    ################### eight notes  ##################################################
    #####in position 1,2,3 of a group of 3 in ternary meter 3/8, 6/8, 9/8 and 12/8#####
    eight_ternary_p1_indexes= get_ternary_eight_indexes(datas, measures_positions, 1)
    eight_ternary_p2_indexes= get_ternary_eight_indexes(datas, measures_positions, 2)
    eight_ternary_p3_indexes= get_ternary_eight_indexes(datas, measures_positions, 3)
    
    
    #for eight notes in position 1,2 of a group of 2 with interleaved voices in binary meter 2/4, 3/4 and 4/4
    eight_interleaved_p1= get_binary_eight_interleaved_indexes(datas, measures_positions, 1)
    eight_interleaved_p2= get_binary_eight_interleaved_indexes(datas, measures_positions, 2)
    
    #for eight notes in position 1,2 of a group of 2 with no voice in binary meter 2/4, 3/4 and 4/4
    eight_no_interleaved_p1= get_binary_eight_not_interleaved_indexes(datas, measures_positions, 1)
    eight_no_interleaved_p2= get_binary_eight_not_interleaved_indexes(datas, measures_positions, 2)
    
    #####results
    results['all']=get_metric_of_selected_elements(metric_data, datas)
    results['no rest']=get_metric_of_selected_elements(metric_data, datas,  rest_filtered=True)
    
    #### voice with paper notation
    results['b']=get_metric_of_selected_elements(metric_data, datas,  select_voice='b')
    results['B']=get_metric_of_selected_elements(metric_data, datas,  select_voice='Bst')
    results['B+b']=get_metric_of_selected_elements(metric_data, datas,  select_voice='Bbst')
    results['u']=get_metric_of_selected_elements(metric_data, datas,  select_voice='u')
    results['m']=get_metric_of_selected_elements(metric_data, datas,  select_voice='m')
    results['x']=get_metric_of_selected_elements(metric_data, datas,  select_voice='x')
     # just for quarter note
    results['♩']=get_metric_of_selected_elements(metric_data, datas,  rest_filtered=True, d=1.0)
    # just for eighth note
    results['♪']=get_metric_of_selected_elements(metric_data, datas,  rest_filtered=True, d=0.5)
    # just for sixteenth note
    results['♬']=get_metric_of_selected_elements(metric_data, datas,  rest_filtered=True, d=0.25)
    
    results['1st beat']=get_metric_of_selected_elements(metric_data, datas, 
                                                     rest_filtered=True, beats_indexes=first_beats)
    # on/off
    results['on beat']=get_metric_of_selected_elements(metric_data, datas, 
                                                    rest_filtered=True, beats_indexes=on_beats)
    
    results['♪ on']=get_metric_of_selected_elements(metric_data, datas,  
                                                rest_filtered=True, d=0.5, beats_indexes=on_beats)
    results['off beat']=get_metric_of_selected_elements(metric_data, datas, 
                                                     rest_filtered=True, beats_indexes=off_beats)
    results['♪ off']=get_metric_of_selected_elements(metric_data, datas,  
                                                  rest_filtered=True, d=0.5, beats_indexes=off_beats)
    #interleaved
    results['1st♪♪ inter BM']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.5, beats_indexes=eight_interleaved_p1)
    results['2nd♪♪ inter BM']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.5, beats_indexes=eight_interleaved_p2)
    #no interleaved
    results['1st♪♪ NO inter BM']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.5, beats_indexes=eight_no_interleaved_p1)
    results['2nd♪♪ NO inter BM']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.5, beats_indexes=eight_no_interleaved_p2)
    ##16th 4-group BM : 
    results['1st♬♬ BM']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.25, beats_indexes=sixteenth_p1_indexes)
    results['2nd♬♬ BM']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.25, beats_indexes=sixteenth_p2_indexes)
    results['3rd♬♬ BM']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.25, beats_indexes=sixteenth_p3_indexes)
    results['4th♬♬ BM']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.25, beats_indexes=sixteenth_p4_indexes)
    ##16th interleaved : 
    results['1st♬♬ interleaved upper/lower']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.25, beats_indexes=sixteenth_p1_indexes_interleaved)
    results['2nd♬♬ interleaved upper/lower']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.25, beats_indexes=sixteenth_p2_indexes_interleaved)
    results['3rd♬♬ interleaved upper/lower']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.25, beats_indexes=sixteenth_p3_indexes_interleaved)
    results['4th♬♬ interleaved upper/lower']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.25, beats_indexes=sixteenth_p4_indexes_interleaved)
    
    #8th 3-group TM
    results['1st♪♪♪ TM']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.5, beats_indexes=eight_ternary_p1_indexes)
    results['2nd♪♪♪ TM']=get_metric_of_selected_elements(metric_data, datas, 
                                                       rest_filtered=True, d=0.5, beats_indexes=eight_ternary_p2_indexes)
    results['3rd♪♪♪ TM']=get_metric_of_selected_elements(metric_data, datas, 
                                                      rest_filtered=True, d=0.5, beats_indexes=eight_ternary_p3_indexes)

    return results


def timings(metric: str, performer: str=None, metric_data: list[float]=None, 
                   datas: list=None)->dict[str:dict[str:list]]:
    """Returns all metric values for all categories used in the web app for one or all performers
    
    Args:
        - metric :name of chosen metric
        - performer : name of a performer. Defaults to  None : all performers)
        - metric_data :  deltasioi  or deltasonsets values
        - datas: corresponding data

    Returns:
        {performer : {group : metric values}}
    """
    performers_res=dict()
    # one specific performer
    if performer!=None:
        results=get_metric_results(metric_data, datas)
        performers_res[performer] = dict()
        for r in results:
            performers_res[performer][r]=results[r]
        return performers_res
    else :# all performers
        res = get_all_perfs(metric) 
        for p in res.keys():
            performers_res[p]=dict()
            results=get_metric_results(res[p][metric], res[p]['data'])
            for r in results:
                performers_res[p][r]=results[r]
        return performers_res



#####################################
#stats
######################################

def produce_stat(tab)->tuple[int, float, float, float, float, float, float, float]:
    """Returns statistics from a population of metric values

    Args:
        - tab: metric values

    Returns:
        Number of elements, mean, 1st-2nd and 3rd quartile, minimum, maximum, standard deviation 
    """
    mean_tab = mean(tab) if len(tab)>0 else 0
    maxi= max(tab) if len(tab)!=0 else 0
    mini = min(tab) if len(tab)!=0 else 0
    q1, q2, q3 = quantiles(tab,n=4) if len(tab)>=2 else [0,0,0] # Statistics Error raised if less than 2 values
    n = len(tab)
    stdev = pstdev(tab) if len(tab)>0 else 0
    return n, mean_tab, q1, q2, q3, mini, maxi, stdev


def results_to_stats(results: dict[str:dict[str:list]])->dict:
    """Returns statistics from all population  groups of metric values

    Args:
        - All metric values for all categories used in the web app
        
    Returns:
        dico format
        d= {key : [n_elements, mean, q1, q2, q3, mini, maxi, stdev]}
    """
    stats=dict()
    for k in results:
        stats[k]=produce_stat(results[k])
    return stats