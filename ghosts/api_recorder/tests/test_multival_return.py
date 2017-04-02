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
def winner_between(x, y, a='Ants', b='Aliens'):
    mals_order = ['Ants','Mice','Rats','Cats','Dogs','Pigs','Cows','Bears','Dinosaurs','Aliens',]

    a_strength = (mals_order.index(a) * mals_order.index(a))
    a_combined_strength = a_strength * x

    b_strength = (mals_order.index(b) * mals_order.index(b))
    b_combined_strength = b_strength * y

    winner = a if a_combined_strength > b_combined_strength else b
    loser = a if winner == b else b

    details = {
                'winner': winner,
                'winner_strength': a_strength if winner == a else b_strength,
                'winner_combined_strength': a_combined_strength if winner == a else b_combined_strength,
                'loser': loser,
                'loser_strength': a_strength if winner == b else b_strength,
                'loser_combined_strength': a_combined_strength if winner == b else b_combined_strength,
                }
    print(details)
    return winner, loser, details


def test_multival_return():

    scenario_name = 'test_complex_input'
    start_recording_scenario(site_name, scenario_name)

    winner1, loser1, details1 = winner_between(8, 3, a='Dogs', b='Dinosaurs')
    winner2, loser2, details2 = winner_between(1, 13, a='Cats', b='Rats')
    winner3, loser3, details3 = winner_between(1000000, 13, a='Mice', b='Bears')

    assert winner1 == 'Dinosaurs'
    assert loser2 == 'Cats'
    assert winner3 == 'Mice'
    assert details3['winner_combined_strength'] > details3['loser_combined_strength']
    assert details3['loser_strength'] > details3['winner_strength']

    end_and_save_scenario(site_name, scenario_name)

    load_scenario(site_name, scenario_name)

    winner1, loser1, details1 = winner_between(8, 3, a='Dogs', b='Dinosaurs')
    winner2, loser2, details2 = winner_between(1, 13, a='Cats', b='Rats')
    winner3, loser3, details3 = winner_between(1000000, 13, a='Mice', b='Bears')

    assert winner1 == 'Dinosaurs'
    assert loser2 == 'Cats'
    assert winner3 == 'Mice'
    assert details3['winner_combined_strength'] > details3['loser_combined_strength']
    assert details3['loser_strength'] > details3['winner_strength']

    unload_scenario(site_name, scenario_name)
