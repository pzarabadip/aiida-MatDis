# -*- coding: utf-8 -*-
"""Copied from aiida-lsmo utils"""
from .ff_builder_module import ff_builder
from .multiply_unitcell import get_replciation_factors
from .general import (get_molecules_input_dict,
                      get_molecule_dict,
                      get_ff_parameters,
                      get_atomic_radii,
                      get_geometric_output,
                      get_pressure_list,
                      choose_pressure_points,
                      get_output_parameters,
                      get_vlcc_output,
                      get_temperature_points,
                      extract_merge_outputs,
                      update_components,
                      modify_zeopp_parameters,
                      modify_pm_parameters,
                      extract_wrap_results)
from .other import update_workchain_params, dict_merge
