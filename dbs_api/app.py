########################################################################################################################
# --- Imports

import os

import pandas as pd

from flask import Flask
from flask import request

########################################################################################################################
# --- Utils

path_to_dir = os.path.dirname(os.path.abspath(__file__))
path_to_outputs = os.path.join(path_to_dir, 'outputs')


########################################################################################################################
# --- App instantiation and landing page

app = Flask(__name__)


@app.route(
    '/',
    methods=['GET']
)
def get_landing_page():
    return 'Hello! Welcome to the adjusted sales mapping API. Documentation is here:'


########################################################################################################################
# --- Main routes

@app.route(
    '/US_sales_mapping',
    methods=['GET']
)
def get_adjusted_US_sales_mapping():

    year = request.args.get('year', default=2018, type=int)

    if year not in [2016, 2017, 2018, 2019]:
        raise Exception('The adjusted sales mapping for US multinationals is only available from 2016 to 2019.')

    sales_mapping = pd.read_csv(
        os.path.join(
            path_to_outputs,
            f'sales_mapping_US_{year}.csv'
        )
    )

    return sales_mapping.to_json()


@app.route(
    '/global_sales_mapping',
    methods=['GET']
)
def get_adjusted_global_sales_mapping():

    year = request.args.get('year', default=2017, type=int)

    if year not in [2016, 2017]:
        # return "The adjusted sales mapping based on the OECD's data is only available for 2016 and 2017."
        raise Exception("The adjusted sales mapping based on the OECD's data is only available for 2016 and 2017.")

    scope_suffix = request.args.get('scope', default='restricted', type=str)

    if scope_suffix not in ['restricted', 'unrestricted']:
        raise Exception(
            "The 'scope' argument can only take two values. If you choose 'restricted', the set of headquarter "
            + "countries will be restricted to the 15 parent jurisdictions that provide a sufficiently granular "
            + "bilateral breakdown via the OECD. If you choose 'unrestricted', all parent countries are included."
        )

    sales_mapping = pd.read_csv(
        os.path.join(
            path_to_outputs,
            f'sales_mapping_{"global_" + scope_suffix}_{year}.csv'
        )
    )

    return sales_mapping.to_json()


########################################################################################################################
# --- Auxiliary routes used in the web application

@app.route(
    '/US_intermediary_dataframe_1',
    methods=['GET']
)
def get_US_intermediary_dataframe_1():

    year = request.args.get('year', default=2018, type=int)

    if year not in [2016, 2017, 2018, 2019]:
        raise Exception('The first intermediary DataFrame for US multinationals is only available from 2016 to 2019.')

    intermediary_dataframe_1 = pd.read_csv(
        os.path.join(
            path_to_outputs,
            f'intermediary_dataframe_1_US_{year}.csv'
        )
    )

    return intermediary_dataframe_1.to_json()


@app.route(
    '/US_intermediary_dataframe_2',
    methods=['GET']
)
def get_US_intermediary_dataframe_2():

    year = request.args.get('year', default=2018, type=int)

    if year not in [2016, 2017, 2018, 2019]:
        raise Exception('The second intermediary DataFrame for US multinationals is only available from 2016 to 2019.')

    intermediary_dataframe_2 = pd.read_csv(
        os.path.join(
            path_to_outputs,
            f'intermediary_dataframe_2_US_{year}.csv'
        )
    )

    return intermediary_dataframe_2.to_json()


@app.route(
    '/global_intermediary_dataframe_1',
    methods=['GET']
)
def get_global_intermediary_dataframe_1():

    year = request.args.get('year', default=2017, type=int)

    if year not in [2016, 2017]:
        raise Exception("The first intermediary DataFrame based on OECD data is only available for 2016 and 2017.")

    intermediary_dataframe_1 = pd.read_csv(
        os.path.join(
            path_to_outputs,
            f'intermediary_dataframe_1_global_restricted_{year}.csv'
        )
    )

    return intermediary_dataframe_1.to_json()


@app.route(
    '/global_intermediary_dataframe_2',
    methods=['GET']
)
def get_global_intermediary_dataframe_2():

    year = request.args.get('year', default=2017, type=int)

    if year not in [2016, 2017]:
        raise Exception("The second intermediary DataFrame based on OECD data is only available for 2016 and 2017.")

    intermediary_dataframe_2 = pd.read_csv(
        os.path.join(
            path_to_outputs,
            f'intermediary_dataframe_2_global_restricted_{year}.csv'
        )
    )

    return intermediary_dataframe_2.to_json()
