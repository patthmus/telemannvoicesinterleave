# -*- coding: utf-8 -*-

"""
This module defines music21 tools to analyse a score
"""

from src.data import MXLS
from music21 import converter, stream

    
#############################################
# score converter
#############################################   
def score(n: int, start: int, end: int)-> stream.Score:
    """Returns a slice of music21 Score 

    Args:
        - n: fantasia number
        - start: starting measure number 
        - end: last measure number

    Returns:
        music21 Score
    """
    score: stream.Score = converter.parse(MXLS[n])
    xml_data: stream.Score = score.measures(start, end, indicesNotNumbers=True) 
    # indicesindicesNotNumbers to avoid the same numbers in an other movement
    # range (start, end) inclusive
    return xml_data
