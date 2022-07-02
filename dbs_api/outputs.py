import os

from destination_based_sales.analyses_provider import USAnalysesProvider, GlobalAnalysesProvider

if __name__ == '__main__':

    path_to_dir = os.path.dirname(os.path.abspath(__file__))
    path_to_outputs = os.path.join(path_to_dir, 'outputs')

    for scope in ['US', 'global_restricted', 'global_unrestricted']:
        available_years = [2016, 2017, 2018, 2019] if scope == 'US' else [2016, 2017]

        for year in available_years:

            print(scope, '-', year, '-', 'loading the data...')

            if scope == 'US':
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

            elif scope == 'global_restricted':
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

            else:
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
            sales_mapping.to_csv(
                os.path.join(path_to_outputs, f'sales_mapping_{scope}_{year}.csv'),
                index=False
            )

            if scope == 'US':
                intermediary_df_1 = analyses_provider.get_intermediary_dataframe_1(
                    include_macro_indicator=True
                )
                intermediary_df_1.to_csv(
                    os.path.join(path_to_outputs, f'intermediary_dataframe_1_{scope}_{year}.csv'),
                    index=False
                )

                intermediary_df_2 = analyses_provider.get_intermediary_dataframe_2(
                    include_macro_indicator=True
                )
                intermediary_df_2.to_csv(
                    os.path.join(path_to_outputs, f'intermediary_dataframe_2_{scope}_{year}.csv'),
                    index=False
                )

                irs = analyses_provider.irs.copy()
                irs.to_csv(
                    os.path.join(path_to_outputs, f'irs_{year}.csv'),
                    index=False
                )

            else:
                intermediary_df_1 = analyses_provider.get_intermediary_dataframe_1(
                    exclude_US_from_parents=False,
                    include_macro_indicator=True,
                )
                intermediary_df_1.to_csv(
                    os.path.join(path_to_outputs, f'intermediary_dataframe_1_{scope}_{year}.csv'),
                    index=False
                )

                intermediary_df_2 = analyses_provider.get_intermediary_dataframe_2(
                    exclude_US_from_parents=False,
                    include_macro_indicator=True
                )
                intermediary_df_2.to_csv(
                    os.path.join(path_to_outputs, f'intermediary_dataframe_2_{scope}_{year}.csv'),
                    index=False
                )

                oecd = analyses_provider.oecd.copy()
                scope_suffix = scope.split('_')[1]
                oecd.to_csv(
                    os.path.join(path_to_outputs, f'oecd_{year}_{scope_suffix}.csv'),
                    index=False
                )

            print(scope, '-', year, '-', 'files saved!')
            print('------------------------------------')
