import os

import numpy as np
import pandas as pd

from destination_based_sales.analyses_provider import USAnalysesProvider, GlobalAnalysesProvider


path_to_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path_to_outputs = os.path.join(path_to_dir, 'dbs_api', 'outputs')


def test_output_files_exist():
    file_list = os.listdir(path_to_outputs)

    for scope in ['US', 'global_restricted', 'global_unrestricted']:
        available_years = [2016, 2017, 2018, 2019] if scope == 'US' else [2016, 2017]

        for year in available_years:
            assert f'sales_mapping_{scope}_{year}.csv' in file_list
            assert f'intermediary_dataframe_1_{scope}_{year}.csv' in file_list
            assert f'intermediary_dataframe_2_{scope}_{year}.csv' in file_list

            if scope == 'US':
                assert f'irs_{year}.csv' in file_list

            else:
                scope_suffix = scope.split('_')[1]
                assert f'oecd_{year}_{scope_suffix}.csv' in file_list


def test_US_outputs():
    available_years = [2016, 2017, 2018, 2019]

    for year in available_years:
        analyses_provider = USAnalysesProvider(
            year=year,
            US_merchandise_exports_source='Comtrade',
            US_services_exports_source='BaTIS',
            non_US_merchandise_exports_source='Comtrade',
            non_US_services_exports_source='BaTIS',
            winsorize_export_percs=True,
            non_US_winsorizing_threshold=0.5,
            US_winsorizing_threshold=0.5,
            service_flows_to_exclude=[],
            macro_indicator='CONS',
            load_data_online=False
        )

        sales_mapping = analyses_provider.sales_mapping.copy()
        sales_mapping_saved = pd.read_csv(
            os.path.join(path_to_outputs, f'sales_mapping_US_{year}.csv')
        )

        intermediary_df_1 = analyses_provider.get_intermediary_dataframe_1(
            include_macro_indicator=True
        ).reset_index(drop=True)
        intermediary_df_1_saved = pd.read_csv(
            os.path.join(path_to_outputs, f'intermediary_dataframe_1_US_{year}.csv')
        )

        intermediary_df_2 = analyses_provider.get_intermediary_dataframe_2(
            include_macro_indicator=True
        ).reset_index(drop=True)
        intermediary_df_2_saved = pd.read_csv(
            os.path.join(path_to_outputs, f'intermediary_dataframe_2_US_{year}.csv')
        )

        irs = analyses_provider.irs.copy()
        irs_saved = pd.read_csv(os.path.join(path_to_outputs, f'irs_{year}.csv'))

        for idx in [0, 1]:
            assert sales_mapping.shape[idx] == sales_mapping_saved.shape[idx]
            assert intermediary_df_1.shape[idx] == intermediary_df_1_saved.shape[idx]
            assert intermediary_df_2.shape[idx] == intermediary_df_2_saved.shape[idx]
            assert irs.shape[idx] == irs_saved.shape[idx]

        for column in ['UNRELATED_PARTY_REVENUES', 'RELATED_PARTY_REVENUES', 'TOTAL_REVENUES']:
            assert np.abs(
                (sales_mapping[column] - sales_mapping_saved[column]) / sales_mapping_saved[column] * 100
            ).max() < 0.00001
            assert np.abs(
                (irs[column] - irs_saved[column]) / irs_saved[column] * 100
            ).max() < 0.00001

        for column in [
            'SHARE_OF_UNRELATED_PARTY_REVENUES',
            'SHARE_OF_RELATED_PARTY_REVENUES',
            'SHARE_OF_TOTAL_REVENUES',
            f'SHARE_OF_CONS_{year}'
        ]:
            assert np.abs(intermediary_df_1[column] - intermediary_df_1_saved[column]).max() < 0.0000001
            assert np.abs(intermediary_df_2[column] - intermediary_df_2_saved[column]).max() < 0.0000001


def test_global_restricted_outputs():
    available_years = [2016, 2017]

    for year in available_years:
        analyses_provider = GlobalAnalysesProvider(
            year=year,
            aamne_domestic_sales_perc=True,
            breakdown_threshold=60,
            US_merchandise_exports_source='Comtrade',
            US_services_exports_source='BaTIS',
            non_US_merchandise_exports_source='Comtrade',
            non_US_services_exports_source='BaTIS',
            winsorize_export_percs=True,
            non_US_winsorizing_threshold=0.5,
            US_winsorizing_threshold=0.5,
            service_flows_to_exclude=[],
            macro_indicator='CONS',
            load_data_online=False
        )

        sales_mapping = analyses_provider.sales_mapping.copy()
        sales_mapping_saved = pd.read_csv(
            os.path.join(path_to_outputs, f'sales_mapping_global_restricted_{year}.csv')
        )

        intermediary_df_1 = analyses_provider.get_intermediary_dataframe_1(
            include_macro_indicator=True,
            exclude_US_from_parents=False
        ).reset_index(drop=True)
        intermediary_df_1_saved = pd.read_csv(
            os.path.join(path_to_outputs, f'intermediary_dataframe_1_global_restricted_{year}.csv')
        )

        intermediary_df_2 = analyses_provider.get_intermediary_dataframe_2(
            include_macro_indicator=True,
            exclude_US_from_parents=False
        ).reset_index(drop=True)
        intermediary_df_2_saved = pd.read_csv(
            os.path.join(path_to_outputs, f'intermediary_dataframe_2_global_restricted_{year}.csv')
        )

        oecd = analyses_provider.oecd.copy()
        oecd = oecd.reset_index(drop=True)
        oecd_saved = pd.read_csv(os.path.join(path_to_outputs, f'oecd_{year}_restricted.csv'))

        for idx in [0, 1]:
            assert sales_mapping.shape[idx] == sales_mapping_saved.shape[idx]
            assert intermediary_df_1.shape[idx] == intermediary_df_1_saved.shape[idx]
            assert intermediary_df_2.shape[idx] == intermediary_df_2_saved.shape[idx]
            assert oecd.shape[idx] == oecd_saved.shape[idx]

        for column in ['UNRELATED_PARTY_REVENUES', 'RELATED_PARTY_REVENUES', 'TOTAL_REVENUES']:
            assert np.abs(
                (
                    (sales_mapping[column] - sales_mapping_saved[column])
                    / sales_mapping_saved[column].map(lambda x: 1 if x == 0 else x)
                    * 100
                )
            ).max() < 0.00001
            assert np.abs(
                (
                    (oecd[column] - oecd_saved[column])
                    / oecd_saved[column].map(lambda x: 1 if x == 0 else x)
                    * 100
                )
            ).max() < 0.00001

        for column in [
            'SHARE_OF_UNRELATED_PARTY_REVENUES',
            'SHARE_OF_RELATED_PARTY_REVENUES',
            'SHARE_OF_TOTAL_REVENUES',
            f'SHARE_OF_CONS_{year}'
        ]:
            assert np.abs(intermediary_df_1[column] - intermediary_df_1_saved[column]).max() < 0.0000001
            assert np.abs(intermediary_df_2[column] - intermediary_df_2_saved[column]).max() < 0.0000001


def test_global_unrestricted_outputs():
    available_years = [2016, 2017]

    for year in available_years:
        analyses_provider = GlobalAnalysesProvider(
            year=year,
            aamne_domestic_sales_perc=True,
            breakdown_threshold=0,
            US_merchandise_exports_source='Comtrade',
            US_services_exports_source='BaTIS',
            non_US_merchandise_exports_source='Comtrade',
            non_US_services_exports_source='BaTIS',
            winsorize_export_percs=True,
            non_US_winsorizing_threshold=0.5,
            US_winsorizing_threshold=0.5,
            service_flows_to_exclude=[],
            macro_indicator='CONS',
            load_data_online=False
        )

        sales_mapping = analyses_provider.sales_mapping.copy()
        sales_mapping_saved = pd.read_csv(
            os.path.join(path_to_outputs, f'sales_mapping_global_unrestricted_{year}.csv')
        )

        intermediary_df_1 = analyses_provider.get_intermediary_dataframe_1(
            include_macro_indicator=True,
            exclude_US_from_parents=False
        ).reset_index(drop=True)
        intermediary_df_1_saved = pd.read_csv(
            os.path.join(path_to_outputs, f'intermediary_dataframe_1_global_unrestricted_{year}.csv')
        )

        intermediary_df_2 = analyses_provider.get_intermediary_dataframe_2(
            include_macro_indicator=True,
            exclude_US_from_parents=False
        ).reset_index(drop=True)
        intermediary_df_2_saved = pd.read_csv(
            os.path.join(path_to_outputs, f'intermediary_dataframe_2_global_unrestricted_{year}.csv')
        )

        oecd = analyses_provider.oecd.copy()
        oecd = oecd.reset_index(drop=True)
        oecd_saved = pd.read_csv(os.path.join(path_to_outputs, f'oecd_{year}_unrestricted.csv'))

        for idx in [0, 1]:
            assert sales_mapping.shape[idx] == sales_mapping_saved.shape[idx]
            assert intermediary_df_1.shape[idx] == intermediary_df_1_saved.shape[idx]
            assert intermediary_df_2.shape[idx] == intermediary_df_2_saved.shape[idx]
            assert oecd.shape[idx] == oecd_saved.shape[idx]

        for column in ['UNRELATED_PARTY_REVENUES', 'RELATED_PARTY_REVENUES', 'TOTAL_REVENUES']:
            assert np.abs(
                (
                    (sales_mapping[column] - sales_mapping_saved[column])
                    / sales_mapping_saved[column].map(lambda x: 1 if x == 0 else x)
                    * 100
                )
            ).max() < 0.00001
            assert np.abs(
                (
                    (oecd[column] - oecd_saved[column])
                    / oecd_saved[column].map(lambda x: 1 if x == 0 else x)
                    * 100
                )
            ).max() < 0.00001

        for column in [
            'SHARE_OF_UNRELATED_PARTY_REVENUES',
            'SHARE_OF_RELATED_PARTY_REVENUES',
            'SHARE_OF_TOTAL_REVENUES',
            f'SHARE_OF_CONS_{year}'
        ]:
            assert np.abs(intermediary_df_1[column] - intermediary_df_1_saved[column]).max() < 0.0000001
            assert np.abs(intermediary_df_2[column] - intermediary_df_2_saved[column]).max() < 0.0000001
