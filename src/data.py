import csv

################
# folders/files
################

ALIGNMENTS = "data/alignments"
PDFS = "data/scores"

MXLS =     {1: 'data/mxl/TelemannWV40.02.mxl',
            2: 'data/mxl/TelemannWV40.03.mxl',
            3: 'data/mxl/TelemannWV40.04.mxl',
            4: 'data/mxl/TelemannWV40.05.mxl',
            5: 'data/mxl/TelemannWV40.06.mxl',
            6: 'data/mxl/TelemannWV40.07.mxl',
            7: 'data/mxl/TelemannWV40.08.mxl',
            8: 'data/mxl/TelemannWV40.09.mxl',
            9: 'data/mxl/TelemannWV40.10.mxl',
            10: 'data/mxl/TelemannWV40.11.mxl',
            11: 'data/mxl/TelemannWV40.12.mxl',
            12: 'data/mxl/TelemannWV40.13.mxl'}


######################################################
# PERFORMERS / MOVEMENTS
######################################################

PERFORMERS = ['kuijken', 'lazarevitch', 'pahud', 'pitelina', 'porter', 'rampal']

# [start;end] :  boundaries included for each movement of each fantasia 
MOVEMENTS = {1: ((1, 10), (11, 26), (27, 36), (37, 63)),
            2: ((1, 11), (12, 59), (60, 68), (69, 110)),
            3: ((1, 2), (3, 17), (18, 21), (22, 32), (33, 75)),
            4: ((1, 14), (15, 69), (70, 97)),
            5: ((1, 5), (6, 9), (10, 14), (15, 26), (27, 80), (81, 118)),
            6: ((1, 32), (33, 64), (65, 100)),
            7: ((1, 14), (15, 85), (86, 96), (97, 130)),
            8: ((1, 17), (18, 48), (49, 72)),
            9: ((1, 29), (30, 79), (80, 83), (84, 125)),
            10: ((1, 56), (57, 121), (122, 145)),
            11: ((1, 26), (27, 28), (29, 57), (58, 85)),
            12: ((1, 4), (5, 24), (25, 28), (29, 55), (56, 61), (62, 69), (70, 129))}


MOVEMENTS_NAMES_BY_FANTASIA = {1: ("toccata", "vivace fugato", "cadence", "passepied"),
            2: ("prelude", "vivace fugato", "adagio", "bourrée"),
            3: ("largo", "vivace fugato", "largo",  "vivace fugato", "gigue"),
            4: ("andante", "polonaise", "aria da capo"),
            5: ("toccata", "récitatif", "toccata", "récitatif", "gigue fugato", "canarie"),
            6: ("adagio", "allegro fugato", "rondo"),
            7: ("largo", "allegro fugato", "largo", "rondo"),
            8: ("allemande", "gigue fugato", "polonaise"),
            9: ("sarabande", "allegro fugato", "sarabande", "bourrée"),
            10: ("corrente", "presto fugato", "menuet"),
            11: ("prelude", "cadence", "vivace fugato", "gigue"),
            12: ("grave", "toccata", "grave", "toccata", "dolce", "allegro", "rigaudon")}



# by {movement_name:{fantasia:[movements numbers]}}
MOVEMENTS_POSITIONS = {'toccata': {1: [1], 5: [1, 3], 12: [2, 4]}, 
                       'adagio': { 2: [3], 6: [1]}, 
                       'passepied': {1: [4]}, 
                       'prelude': {2: [1], 11: [1]},
                       'vivace fugato': {1: [2], 2: [2], 3: [2, 4], 11: [3]}, 
                       'bourrée': {2: [4], 9: [4]}, 
                       'largo': {3: [1, 3], 7: [1, 3]}, 
                       'gigue': {3: [5], 11: [4]}, 
                       'andante': {4: [1]}, 
                       'polonaise': {4: [2], 8: [3]}, 
                       'aria da capo': {4: [3]}, 
                       'récitatif': {5: [2, 4]}, 
                       'gigue fugato': {5: [5], 8: [2]},
                       'canarie': {5: [6]}, 
                       'allegro fugato': {6: [2], 7: [2], 9: [2]},
                       'rondo': {6: [3], 7: [4]},
                       'allemande': {8: [1]}, 
                       'sarabande': {9: [1, 3]}, 
                       'courante': {10: [1]}, 
                       'presto fugato': {10: [2]},
                       'menuet': {10: [3]}, 
                       'cadence': {1: [3], 11: [2]},
                       'grave': {12: [1, 3]},
                       'dolce': {12: [5]},
                       'allegro': {12: [6]}, 
                       'rigaudon': {12: [7]}}


##########################################################
# MEASURES SEQUENCES
##########################################################

# SEQUENCES OF NOTES (start,end,repetitionnumber) :  boundaries included - for audio synchronization
SEQUENCES_WITH_REPEATS = {1: (MOVEMENTS[1][0] + (0,), MOVEMENTS[1][1]+ (0,), MOVEMENTS[1][2]+ (0,),
                              (37, 48, 0), (37, 48, 1), (49,62, 0), (49,61, 1), (63, None, 0)
                             ),
                          2: (MOVEMENTS[2][0]+ (0,), MOVEMENTS[2][1]+ (0,), MOVEMENTS[2][2]+ (0,),
                             (69, 87, 0), (69, 87, 1), (88, 110, 0), (88, 110, 1)
                             ),
                          3: (MOVEMENTS[3][0]+ (0,), MOVEMENTS[3][1]+ (0,), MOVEMENTS[3][2]+ (0,), MOVEMENTS[3][3]+ (0,), 
                              (33, 55, 0), (33, 55, 1), (56, 75, 0), (56, 75, 1)
                             ),
                          4: (MOVEMENTS[4][0]+ (0,), MOVEMENTS[4][1]+ (0,),
                              (70, 81, 0), (70, 81, 1), (82, 97, 0), (70, 81, 2)
                             ),
                          5: (MOVEMENTS[5][0]+ (0,), MOVEMENTS[5][1]+ (0,), 
                              MOVEMENTS[5][2]+ (0,), MOVEMENTS[5][3]+ (0,), MOVEMENTS[5][4]+ (0,),
                              (81, 95,0), (81, 95,1), (96, 118,0), (96, 118,1)
                              ),
                          6: ((1, 15,0), (1, 15,1), (16, 32,0), (16, 32,1),
                              MOVEMENTS[6][1]+ (0,),
                              (65, 100,0), (65, 70,1)
                             ),
                          7: ((1, 14,0), (1, 13,1), 
                              (15, 85,0),        # mvt 2
                              (86, 94,0),        # mvt 3
                              (95, None,0), (16, 85,1), # mvt 2
                              (86, 94,1), (96, None,0), # mvt 3
                              (97, 130,0), (97, 105,1)
                              ),
                          8:(MOVEMENTS[8][0]+ (0,), MOVEMENTS[8][1]+ (0,),
                             (49, 56,0), (49, 56,0), (57, 72,0), (57, 72,1)
                             ),
                          9:((1, 13,0), (1, 13,1), (14, 29,0), (14, 29,1),
                             MOVEMENTS[9][1]+ (0,), MOVEMENTS[9][2]+ (0,),
                             (84, 100,0), (84, 100,1), (101, 125,0), (101, 125,1)
                             ),
                          10:((1, 23,0), (1, 23,1), (24, 56,0), (24, 56,1),
                              MOVEMENTS[10][1]+ (0,),
                              (122, 129,0), (122, 129,1), (130, 145,0), (130, 145,1)
                              ),
                          11:(MOVEMENTS[11][0]+ (0,), MOVEMENTS[11][1]+ (0,), MOVEMENTS[11][2]+ (0,),
                              (58, 70,0), (58, 70,1), (71, 85,0), (71, 85,1)
                              ),
                          12:(MOVEMENTS[12][0]+ (0,), MOVEMENTS[12][1]+ (0,), MOVEMENTS[12][2]+ (0,), 
                              MOVEMENTS[12][3]+ (0,), MOVEMENTS[12][4]+ (0,),MOVEMENTS[12][5]+ (0,),
                              (70, 78,0), (70, 78,1), (79, 87,0), (79, 87,1), 
                              (88, 108,0), (88, 108,1), (109, 129,0), (109, 129,1), 
                              (70, 78,2), (70, 78,3), (79, 87,2)
                             )
                          }

#alternate performances (f4 :pahud, rampal  -  f2,f3,f5,f6,f7,f9,f10,f12: kuijken )
ALTERNATE_SEQUENCES_1 = {2:(MOVEMENTS[2][0]+ (0,), MOVEMENTS[2][1]+ (0,), MOVEMENTS[2][2]+ (0,),
                             (69, 87, 0), (69, 87, 1), (88, 110, 0)
                             ),

                        3: (MOVEMENTS[3][0]+ (0,), MOVEMENTS[3][1]+ (0,), MOVEMENTS[3][2]+ (0,), MOVEMENTS[3][3]+ (0,), 
                              (33, 55,0), (33, 55,1), (56, 75,0)
                             ),
                        4: (MOVEMENTS[4][0]+ (0,), MOVEMENTS[4][1]+ (0,),
                              (70, 81,0), (70, 81,1), 
                              (82, 97,0), (70, 81,2), (82, 97,1), 
                              (70, 81,3)
                             ),
                        5: (MOVEMENTS[5][0]+ (0,), MOVEMENTS[5][1]+ (0,), MOVEMENTS[5][2]+ (0,), 
                            MOVEMENTS[5][3]+ (0,), MOVEMENTS[5][4]+ (0,),
                              (81, 95,0), (81, 95,1), (96, 118,0)
                              ),
                        6: ((1, 15,0), (1, 15,1), (16, 32,0),
                              MOVEMENTS[6][1]+ (0,),
                              (65, 100,0), (65, 70,1)
                             ),
                        7: ((1, 14,0), (1, 13,1), 
                              (15, 85,0),        
                              (86, 94,0),        
                              (96, None,0), 
                              (97, 130,0), (97, 105,1)
                              ),
                        9:((1, 13,0), (1, 13,1), (14, 29,0), 
                             MOVEMENTS[9][1]+ (0,), MOVEMENTS[9][2]+ (0,),
                             (84, 100,0), (84, 100,1), (101, 125,0)
                             ),
                        10:((1, 23,0), (1, 23,1), (24, 56,0),
                              MOVEMENTS[10][1]+ (0,),
                              (122, 129,0), (122, 129,1), (130, 145,0), (130, 145,1)
                              ),
                        
                        12:(MOVEMENTS[12][0]+ (0,), MOVEMENTS[12][1]+ (0,), MOVEMENTS[12][2]+ (0,), 
                            MOVEMENTS[12][3]+ (0,), MOVEMENTS[12][4]+ (0,),MOVEMENTS[12][5]+ (0,),
                              (70, 78,0), (70, 78,1), (79, 87,0), (79, 87,1), 
                              (88, 108,0), (88, 108,1), (109, 129,0), 
                              (70, 78,2), (70, 78,3), (79, 87,2)
                             ),
                        }
                        
#alternate performances ( f12 porter)
ALTERNATE_SEQUENCES_2 = {12: (MOVEMENTS[12][0]+ (0,), MOVEMENTS[12][1]+ (0,), MOVEMENTS[12][2]+ (0,), 
                              MOVEMENTS[12][3]+ (0,), MOVEMENTS[12][4]+ (0,),MOVEMENTS[12][5]+ (0,),
                              (70, 78,0), (70, 78,1), (79, 87,0), (79, 87,1), 
                              (88, 108,0), (88, 108,1), (109, 129,0), (109, 129,1), 
                              (70, 78,2), 
                              (79, 87,2)
                             )
                          }

#alternate performances ( f12 pahud, pitelina, rampal, lazarevitch)
ALTERNATE_SEQUENCES_3 = {12: (MOVEMENTS[12][0]+ (0,), MOVEMENTS[12][1]+ (0,), MOVEMENTS[12][2]+ (0,), 
                              MOVEMENTS[12][3]+ (0,), MOVEMENTS[12][4]+ (0,),MOVEMENTS[12][5]+ (0,),
                              (70, 78,0), (70, 78,1), (79, 87,0), (79, 87,1), 
                              (88, 108,0), (88, 108,1), (109, 129,0), (109, 129,1), 
                              (70, 78,2), (70, 78,3), (79, 87,2), (79, 87,3)
                             )
                          }
                          
######by performers::
MEASURES_BY_PERFORMERS = {'kuijken':{i:SEQUENCES_WITH_REPEATS[i] if not (i in [2,3,5,6,7,9,10,12]) else 
                                     ALTERNATE_SEQUENCES_1[i] 
                                     for i in range(1,13) },
                       'lazarevitch':{i:SEQUENCES_WITH_REPEATS[i] if i!=12 else 
                                ALTERNATE_SEQUENCES_3[i]
                                for i in range(1,13)},
                       'pahud':{i:SEQUENCES_WITH_REPEATS[i] if not (i in [4,12]) else 
                                ALTERNATE_SEQUENCES_1[i] if i==4 else 
                                ALTERNATE_SEQUENCES_3[i]
                                for i in range(1,13)},
                       'pitelina':{i:SEQUENCES_WITH_REPEATS[i] if i!=12 else 
                                ALTERNATE_SEQUENCES_3[i]
                                for i in range(1,13)},
                       'porter': {i:SEQUENCES_WITH_REPEATS[i] if i!=12 else 
                                  ALTERNATE_SEQUENCES_2[12] for i in range(1,13) },
                       'rampal':{i:SEQUENCES_WITH_REPEATS[i] if not (i in [4,12]) else 
                                ALTERNATE_SEQUENCES_1[i] if i==4 else 
                                ALTERNATE_SEQUENCES_3[i]
                                for i in range(1,13)}
                       }


ENDS = {k:MOVEMENTS[k][-1][1] for k in range(1,13)}

##########################################################
# FUGATOS SEQUENCES
##########################################################

FUGATOS = {1: (MOVEMENTS[1][1] + (0,),),
        2: (MOVEMENTS[2][1]+(0,),),
        3: (MOVEMENTS[3][1]+(0,), MOVEMENTS[3][3]+(0,)),
        4: ((0, 0, 0),),
        5: (MOVEMENTS[5][4] + (0,),),
        6: (MOVEMENTS[6][1]+ (0,),),
        7: ((15, 85,0),(95, None,0), (16, 85,1)),
        8: (MOVEMENTS[8][1]+ (0,),),
        9: (MOVEMENTS[9][1]+ (0,),),
        10: (MOVEMENTS[10][1]+ (0,),),
        11: (MOVEMENTS[11][2]+ (0,),),
        12:((0, 0, 0),)}

# Difference only with Kuijken on Fantasia n°7
ALTERNATE_FUGATOS = {7: ((15, 85,0),)}


MEASURES_FUGATOS_BY_PERFORMERS = {'kuijken' : {i:FUGATOS[i] if i!= 7 else ALTERNATE_FUGATOS[i] for i in range(1,13) },
                                 'lazarevitch':FUGATOS,
                                 'pahud':FUGATOS,
                                 'pitelina':FUGATOS,
                                 'porter': FUGATOS,
                                 'rampal':FUGATOS}


##########################################################
# YOUTUBE VIDEOS URLS ID
##########################################################

YT_ID= {'kuijken' :{1: '8yK7jBcQmJ4',
                          2: 'naomMhbdmrM',
                          3: '6bxrB72Y3ww',
                          4: 'aCXZuA234N8',
                          5: 'Qhg-971Hksk',
                          6: 'YIO-MPL6c2E',
                          7: 'A1JIDyQwdZY',
                          8: 'Kyc_bvQiCnE',
                          9: 'dwk9oCkpAjo',
                          10: 'Gt2RAD-Rghw',
                          11: 'qE_CCQLs6kE',
                          12: 'EPTgofxKZPI'},
              'lazarevitch' :{1:'SZwfLY0hxS8' ,
                          2: 'qVQfkPMhfUw',
                          3: 'tOE0usBzhM4',
                          4: 'JNycILzdCmM',
                          5: 'kq8FOSsL1_k',
                          6: 'oA_Bm00Fq3A',
                          7: 'Lbd-yTki_gI',
                          8: 'gKEPoTwa0Cs',
                          9: 'V-6qAMcTQFQ',
                          10: '4MhEGkj2X50',
                          11: 'fFyNcWnGs9I',
                          12: 'A9c8Y12zT04'},
              'pahud' :{1: 'nX_3CZ-k29U',
                          2: 'KI7UKiVPF8E',
                          3: 'zMFziSa-d2M',
                          4: 'ULrbSrZn6Jw',
                          5: 'P2MOrzq9WzQ',
                          6: '2z0MH_vXVII',
                          7: 'urcyaOrpOhI',
                          8: 'NT_98_bfyJQ',
                          9: 'JeCQr9UVYnk',
                          10: 'RbBlBoV-QQg',
                          11: 'e9ndBU6CkWI',
                          12: 'fzrgM5Qgbk8'},
              'pitelina' :{1: '80f0-jMLcVg',
                          2: 'Cz7dXlX7Kd4',
                          3: 'IKnLAkZNp_Q',
                          4: '1eYa7LzLvu4',
                          5: 'wI4E_zWPOto',
                          6: 'Uy7zm9nUqt0',
                          7: 'Ykrkq1a2pmU',
                          8: 'IXQMiu1uEAM',
                          9: 'Ycz5HUIHLPc',
                          10: 'P8QoBL1dATs',
                          11: 'jzZ6VPSWZK8',
                          12: 'kc48KF6_uKA' },
              'porter' :{1: '-Ik72z2ASkE',
                          2: 'EBXw-XLwXZ4',
                          3: 'kU_7aBWIyes',
                          4: 'UFPMjZ6WK0s',
                          5: 'trg4TYyqfV8',
                          6: 'j0l5ixmLQ-8',
                          7: '00w4_aOcnAU',
                          8: 'tSBd9ZzilLo',
                          9: 'IvQE4ogZIJw',
                          10: 'WH0lkmI49NY',
                          11: 'iVqd_O6qV3A',
                          12: 'SfYxxKg71Ok'},
              'rampal' :{1: 'Pt9C2F0FLrI',
                          2: 'tm6XpC7hCpU',
                          3: 'cMHfw6ceIyg',
                          4: 'QpZC-IiEZdY',
                          5: 'g0-8ncbag6w',
                          6: 'uOIKGm9_RMc',
                          7: '3-H0vnusYng',
                          8: 'uzcGGKPptSY',
                          9: 'l1zwhavkCyc',
                          10: 'xM95bqbraio',
                          11: 'd_myETgatbw',
                          12: '0AOx5OubzZY'}
}


#######################################
## MAIN FUCNTIONS
#######################################

def get_all_data(performer: str, fantasia: str)->list[dict[str:str]]:
    """Produce a dictionnary from a csv file corresponding to an alignment

    Args:
        performer: name of the performer
        fantasia: fantasia's number
    Returns:
        list of dictionnaries (each corresponding to a note or a rest) with the folowing keys : 
        - 'pitchname'
        - 'onset'
        - 'ioi' 
        - 'duration'
        - 'time_signature'
        - 'voice'
        - 'fantasia'
        - 'movement'
        - 'measure'
        - 'repeated'
    """
    data = []
    with open(f'{ALIGNMENTS}/{performer}/alignment_{fantasia}.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            data.append({'pitchname':row['Note'],
                        'onset': row['Onset (ms)'],
                        'ioi': row['Time_duration (ms)'],
                        'duration' : row['Score_duration'],
                        'time_signature': row['Time-Signature'],
                        'voice': row['Voice'],
                        'fantasia': fantasia,
                        'movement': row['Movement'],
                        'measure': row['Measure'],
                        'repeated': row['Repeated']
                        })
    return data


def get_feature(data: list[dict[str:str]], feature: str, filter_value:str)-> list[dict[str:str]]:
    """data corresponding to a performer and a fantasia
    filtered with a given feature value
    
    Args:
        - data
        - feature : pitchname, onset, ioi, 
                duration, time_signature, voice,
                movement, measure, repeated
        - filter_value : value of the feature
    Returns:
        sequence of dictionnary with keys : 
            pitchname, onset, ioi, 
            duration, time_signature, voice,
            movement, measure, repeated
        with only elements with the right feature value given in parameter
    """
    return [e for e in data if e[feature]==filter_value]


def get_data_movement(data: list[dict[str:str]], movement: str)->list[dict[str:str]]:
    """data corresponding to a performer and a fantasia
        and a specific movement

    Args:
        - data: data corresponding to a performer and a fantasia
        - movement: movement number
        
    Returns:
        sequence of dictionnary with keys : 
            pitchname, onset, ioi, 
            duration, time_signature, voice,
            movement, measure, repeated
        with only elements corresponding to a given movement
    """
    return get_feature(data, 'movement', movement)

    
def get_movements_positions()->dict[str:dict[int:list[int]]]:
    """Returns movements positions by name in all fantasia
    used to build MOVEMENTS_POSITIONS

    Returns:
        - {movement_name:{fantasia:[movements numbers]}}
    """
    res={}
    for f in MOVEMENTS_NAMES_BY_FANTASIA:
        mov = list(MOVEMENTS_NAMES_BY_FANTASIA[f])
        for i in range(len(mov)):
            if mov[i] not in res:
                res[mov[i]] = {f:[i+1]}
            else:
                if f not in res[mov[i]]:
                    res[mov[i]][f]=[i+1]
                else:
                    res[mov[i]][f].append(i+1)
    return res