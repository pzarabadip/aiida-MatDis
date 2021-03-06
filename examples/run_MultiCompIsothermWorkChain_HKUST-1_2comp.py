#!/usr/bin/env python  # pylint: disable=invalid-name
# -*- coding: utf-8 -*-
"""Run example two-component isotherm calculation with HKUST1 framework."""

from __future__ import absolute_import
from __future__ import print_function

import os
import click

from aiida.engine import run
from aiida.plugins import DataFactory, WorkflowFactory
from aiida.orm import Code, Dict

# Workchain objects
MultiCompIsothermWorkChain = WorkflowFactory('matdis.multi_comp_isotherm')  # pylint: disable=invalid-name

# Data objects
CifData = DataFactory('cif')  # pylint: disable=invalid-name
NetworkParameters = DataFactory('zeopp.parameters')  # pylint: disable=invalid-name
SinglefileData = DataFactory('singlefile')


@click.command('cli')
@click.argument('zeopp_code_label')
@click.argument('raspa_code_label')
def main(zeopp_code_label, raspa_code_label):
    """
    Prepare inputs and submit the MultiCompIsothermWorkChain for two components.
    Usage: verdi run run_MultiCompIsothermWorkChain_HKUST-1_2comp.py zeopp@teslin raspa37@teslin
    """

    builder = MultiCompIsothermWorkChain.get_builder()

    builder.metadata.label = "test"

    builder.structure = CifData(file=os.path.abspath('../aiida_matdis/data/HKUST-1.cif'), label="hkust1")

    builder.mixture = Dict(dict={
        'comp1': {
            'name': 'xenon',
            'molfraction': 0.20
        },
        'comp2': {
            'name': 'krypton',
            'molfraction': 0.80
        },
    })

    builder.zeopp.code = Code.get_from_string(zeopp_code_label)
    builder.zeopp.atomic_radii = SinglefileData(file=os.path.abspath('../aiida_matdis/data/UFF.rad'))

    builder.raspa_base.raspa.code = Code.get_from_string(raspa_code_label)

    options = {
        "resources": {
            "num_machines": 1,
            "tot_num_mpiprocs": 1,
        },
        "max_wallclock_seconds": 1 * 60 * 60,
        "withmpi": False,
    }
    builder.raspa_base.raspa.metadata.options = options
    builder.zeopp.metadata.options = options



    builder.parameters = Dict(
        dict={
            'ff_framework': 'UFF',  # Default: UFF
            'temperature': 298,  # (K) Note: higher temperature will have less adsorbate and it is faster
            'zeopp_volpo_samples': 100,  # Default: 1e5 *NOTE: default is good for standard real-case!
            'zeopp_sa_samples': 100,  # Default: 1e5 *NOTE: default is good for standard real-case!
            'zeopp_block_samples': 100,  # Default: 100
            'raspa_widom_cycles': 500,  # Default: 1e5
            'raspa_gcmc_init_cycles': 500,  # Default: 1e3
            'raspa_gcmc_prod_cycles': 500,  # Default: 1e4
            'pressure_list': [0.1, 1.0, 2.0],
            "probe_based": False,
        })

    run(builder)


if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter

# EOF
