import os, sys, logging, platform
import xlrd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def check_env_config(file_path, file_name):
    if platform.system() == 'Windows' or platform.system() == 'Darwin':
        file_export_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))), 'DDL')
        if not os.path.exists(os.path.join(file_path, file_name)):
            logger.error(f'Please add {file_name} in path {file_path}')
            sys.exit(-1)
        else:
            return file_export_path
    else:
        logger.error('We do not support Linux, please use windows or mac')
        sys.exit(-1)


def check_table_type(dict_tables):
    if len(dict_tables.get(list(dict_tables.keys())[0])) == dict_tables.get('TABLE_TYPE').count('ORC'):
        logger.info('Table Type check: pass ')
        return
    else:
        logger.error('We do not support any table type other than ORC, please revise')
        sys.exit(-1)


def create_sql_excel(dict_column, dict_table, dict_etl, dict_level, table_name, table_comment):
    new_row = '\n'
    table_database = \
    filter_by_column(dict_level, 'BELONG_LEVEL', dict_table.get('BELONG_LEVEL')).get('TABLE_DATABASE_NAME')[
        0] + '.' if dict_table.get('BELONG_LEVEL') else ''
    cluster_column = filter_by_column(dict_column, 'CLUSTER_COLUMN', 'YES').get('Column Physical Name')

    values = []
    for i in range(len(dict_column.get(list(dict_column.keys())[0]))):
        dict_column_tmp = get_dic_by_index(dict_column, i)
        if dict_column_tmp.get('NOT NULL') == 'Y':
            values.append(
                f"""`{dict_column_tmp.get('Column Physical Name')}` {dict_column_tmp.get('Data Type')} DEFAULT NULL COMMENT {f"'{dict_column_tmp.get('Column Logical Name')}'"} """)
        else:
            values.append(
                f"""`{dict_column_tmp.get('Column Physical Name')}` {dict_column_tmp.get('Data Type')} NOT NULL COMMENT {f"'{dict_column_tmp.get('Column Logical Name')}'"} """)

    list_etl_column = []
    for i in range(len(dict_etl.get(list(dict_etl.keys())[0]))):
        dict_etl_tmp = get_dic_by_index(dict_etl, i)
        list_etl_column.append(
            f"""`{dict_etl_tmp.get('Physical Name')}` {dict_etl_tmp.get('Data Type')} NOT NULL COMMENT {f"'{dict_etl_tmp.get('Logical Name')}'"} """)
    etl_column = f',{new_row}  '.join(list_etl_column)

    if dict_table.get('ETL_PROC') == 'YES':
        values = values + [etl_column]

    sql_drop = f'''DROP TABLE IF EXISTS {table_database}{table_name};'''

    sql = f"""CREATE TABLE {table_database}{table_name} 
    ({f',{new_row}  '.join(values)} ) 
    COMMENT {f"'{table_comment}'"} """

    if dict_table.get('PARTITION_FLAG') == 'YES':
        sql = sql + new_row + dict_table.get('PARTITION_DEF')

    if dict_table.get('CLUSTER_FLAG') == 'YES':
        if dict_table.get('CLUSTER_QUANTITY') != '':
            sql = sql + new_row + f'''    CLUSTERED BY ({','.join(cluster_column)}) 
        INTO {int(dict_table.get('CLUSTER_QUANTITY'))} BUCKETS'''
        else:
            sql = sql + new_row + f'''    CLUSTERED BY ({','.join(cluster_column)}) 
                    INTO 3 BUCKETS'''

    sql = sql + new_row + '   STORED AS ORC;'

    return sql_drop + new_row + sql


def get_target_column(sheet, list_t) -> dict:
    list_value = []
    key = [sheet.cell_value(0, i) for i in range(sheet.ncols)]
    for j in list_t:
        list_value.append(sheet.col_values(key.index(j))[1:])
    return dict(zip(list_t, list_value))


def get_list_by_index(list_o, list_index) -> list:
    list_result = [list_o[i] for i in list_index]
    return list_result


def get_target_column_by_index(sheet, list_index, key=list(), row_star=2) -> dict:
    list_value = []
    if len(key) == 0:
        key = [sheet.cell_value(1, i) for i in range(sheet.ncols)]
    for j in list_index:
        list_value.append(sheet.col_values(j)[row_star:])
    return dict(zip(key, list_value))


def filter_by_column(dict_o, col, value) -> dict:
    dict_result = {}
    list_target_index = []
    list_value = dict_o.get(col)
    if not isinstance(value, list):
        value = [value]
    for i in range(len(list_value)):
        if list_value[i] in value:
            list_target_index.append(i)
        else:
            continue
    for j in dict_o.keys():
        dict_result[j] = get_list_by_index(dict_o.get(j), list_target_index)
    return dict_result


def get_dic_by_index(dict_o, dict_index) -> dict:
    dict_result = {}
    for j in dict_o.keys():
        dict_result[j] = dict_o.get(j)[dict_index]
    return dict_result


def main():
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))), 'Template')
    file_name = '02-MODEL-DATA_DICTIONARY.xlsx'
    file_name_config = '01-MODEL-CONFIGURATION_FILE.xlsx'
    file_export_name = 'GenerateTableDDL.sql'

    logger.info('Check 1: OS check start')
    file_export_path = check_env_config(file_path, file_name)
    check_env_config(file_path, file_name_config)
    logger.info('Check 1: OS check done')

    logger.info('STEP 0: read file start')
    _file = xlrd.open_workbook(os.path.join(file_path, file_name))
    tables = _file.sheet_by_name('Tables')
    columns = _file.sheet_by_name('AllColumns')

    file_config = xlrd.open_workbook(os.path.join(file_path, file_name_config))
    etl = file_config.sheet_by_name('06-ETL_AUDIT')
    level = file_config.sheet_by_name('07-DATA_LAYER')
    logger.info('STEP 0: read file done')

    logger.info('STEP 1: standardize file start')
    tables_target = ['Type'
        , 'Logical Name'
        , 'Name'
        , 'BELONG_LEVEL'
        , 'CLUSTER_FLAG'
        , 'CLUSTER_QUANTITY'
        , 'PARTITION_DEF'
        , 'PARTITION_FLAG'
        , 'ETL_PROC'
        , 'TABLE_TYPE']

    columns_target = ['Table Logical Name'
        , 'Table Physical Name'
        , 'Column Logical Name'
        , 'Column Physical Name'
        , 'Data Type'
        , 'NOT NULL'
        , 'CLUSTER_COLUMN']

    dict_tables = get_target_column(tables, tables_target)
    dict_columns = get_target_column(columns, columns_target)

    dict_tables = filter_by_column(dict_tables, 'Type', 'Table')
    dict_etl = get_target_column_by_index(etl, [0, 1, 2])
    dict_level = get_target_column_by_index(level, [0, 1, 2])
    logger.info('STEP 1: standardize file done')

    logger.info('Check 2: Table type check start')
    check_table_type(dict_tables)
    logger.info('Check 2: Table type check start')

    logger.info('STEP 2: convert to sql start')
    sql_result = ''

    for i in range(len(dict_tables.get(list(dict_tables.keys())[0]))):
        dict_table_tmp = get_dic_by_index(dict_tables, i)
        table_name = dict_table_tmp.get('Name')
        table_comment = dict_table_tmp.get('Logical Name')
        dict_column_tmp = filter_by_column(dict_columns, 'Table Logical Name', dict_table_tmp.get('Logical Name'))
        if len(dict_column_tmp.get(list(dict_column_tmp.keys())[0])) > 0:
            sql_result = sql_result \
                         + f'''/*=================================================*/
/* Table: {table_name} */
/* Definition: {table_comment} */
/*=================================================*/''' + '\n'

            sql_result = sql_result + create_sql_excel(dict_column_tmp
                                                       , dict_table_tmp
                                                       , dict_etl
                                                       , dict_level
                                                       , table_name
                                                       , table_comment) + '\n' + '\n'
        else:
            continue
    logger.info('STEP 2: convert to sql done')

    logger.info('STEP 3: export sql start')
    txt_ddl = open(os.path.join(file_export_path, file_export_name), "w", encoding='utf-8')
    txt_ddl.write(str(sql_result))
    txt_ddl.close()
    logger.info('STEP 3: export sql done')
    logger.info(f'Please find your {file_export_name} in path: {file_export_path}')


if __name__ == '__main__':
    main()
