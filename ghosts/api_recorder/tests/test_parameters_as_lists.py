# -*- encoding: utf-8 -*-
import os
import pytest

from ghosts.api_recorder.api_recorder import api_recorder
from ghosts.api_recorder.tests.recording_management import (
    start_recording_scenario,
    pause_recording_scenario,
    start_healing_scenario,
    restart_recording_scenario,
    end_and_save_scenario,
    scenario_exists,
    load_scenario,
    pause_playback_scenario,
    restart_playback_scenario,
    unload_scenario,
)
from ghosts.api_recorder.tests.scenario import (
    ApiSuperClassDecorated,
    scenario_val,
    api_response,
)

site_name = 'pyghosts'


@api_recorder
def strongest_animal(animals_list):
    mals_order = ['Ants','Mice','Rats','Cats','Dogs','Pigs','Cows','Bears','Dinosaurs','Aliens',]

    report = {}

    strongest = animals_list[0] if animals_list else None
    running_strength = 0

    for animal in animals_list:

        animal_strength = (mals_order.index(animal) * mals_order.index(animal))
        report[animal] = animal_strength

        if animal_strength > running_strength:
            strongest = animal
            running_strength = animal_strength


    details = {
                'winner': strongest,
                'winner_strength': running_strength,
                'report': report,
                }

    return strongest, details


def test_parameters_as_lists():

    scenario_name = 'test_parameters_as_lists'
    start_recording_scenario(site_name, scenario_name)

    rec_winner1, rec_details1 = strongest_animal(['Cats'])
    """One in the list."""
    rec_winner2, rec_details2 =  strongest_animal(['Dinosaurs', 'Dogs', 'Aliens'])
    """Two with same letter."""
    rec_sort1_winner3, rec_sort1_details3 = strongest_animal(['Pigs', 'Mice', 'Cats', 'Dogs', 'Rats'])
    """Sort order 1."""

    assert rec_winner1 == 'Cats'
    """Correct answer."""

    assert rec_winner2 == 'Aliens'
    """Correct answer."""
    assert rec_details2['report']['Dogs'] < rec_details2['report']['Dinosaurs']
    """Presense of details"""

    assert rec_sort1_winner3 == 'Pigs'
    """Correct answer."""
    assert rec_sort1_details3['report']['Rats'] > rec_sort1_details3['report']['Mice']
    """Presense of details"""

    end_and_save_scenario(site_name, scenario_name)

    load_scenario(site_name, scenario_name)

    plyb1_winner1, plyb1_details1 = strongest_animal(['Cats'])
    """Testing Playback of: One in the list."""
    plyb1_winner2, plyb1_details2 =  strongest_animal(['Dinosaurs', 'Dogs', 'Aliens'])
    """Testing Playback of: Two with same letter."""
    plyb1_sort1_winner3, plyb1_sort1_details3 =  strongest_animal(['Pigs', 'Mice', 'Cats', 'Dogs', 'Rats'])
    """Testing Playback of: Sort order 1."""

    assert plyb1_winner1 == rec_winner1
    assert plyb1_winner2 == rec_winner2
    assert plyb1_details2['report']['Dinosaurs']  == rec_details2['report']['Dinosaurs']
    assert rec_sort1_winner3 == rec_sort1_winner3
    assert rec_sort1_details3['report']['Mice']  == rec_sort1_details3['report']['Mice']
    """Everything was playbacked identically."""

    unload_scenario(site_name, scenario_name)

    start_recording_scenario(site_name, scenario_name)

    rec_sort2_winner4, rec_sort2_details4 = strongest_animal(['Dogs', 'Pigs', 'Cats', 'Rats', 'Mice'])
    """Recording: Change the starting order 2."""

    assert rec_sort2_winner4 == plyb1_sort1_winner3
    assert rec_sort2_details4['report']['Dogs'] > plyb1_sort1_details3['report']['Cats']
    """When not playing back, the order of the list makes no difference."""

    end_and_save_scenario(site_name, scenario_name)

    load_scenario(site_name, scenario_name)

    plyb_sort3_winner5, plyb_sort3_details5 = strongest_animal(['Rats', 'Dogs', 'Pigs', 'Mice', 'Cats'])
    """Testing Playback of: Same as above - different starting order 3."""

    assert plyb_sort3_winner5 == rec_sort2_winner4
    assert plyb_sort3_details5['report']['Dogs'] > rec_sort2_details4['report']['Cats']
    """Everything was played back from the signature of the original recording,
    despite the order of the list input.
    """
    unload_scenario(site_name, scenario_name)
