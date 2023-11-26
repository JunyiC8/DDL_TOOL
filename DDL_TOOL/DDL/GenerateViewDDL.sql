/*=================================================*/
/* View: test_table */
/* Definition: Test_Table */
/*=================================================*/
CREATE OR REPLACE VIEW pv_dwd.test_table 
    (`vender_no`  COMMENT 'vender number' ,
  `vender_nm`  COMMENT 'vender name' ,
  `acct_period`  COMMENT 'accounting period' ,
  `pur_qty`  COMMENT 'purchase quantity' ,
  `pur_avg_prc`  COMMENT 'purchase average price' ,
  `pur_amt`  COMMENT 'purchase amount' ,
   `src_db_nm` COMMENT 'source database name' ,
   `src_tab_nm` COMMENT 'source table name' ,
   `etl_job` COMMENT 'ETL process job name' ,
   `etl_tx_dt` COMMENT 'ETL extact date' ,
   `etl_upd_dt` COMMENT 'ETL update date' ,
   `etl_proc_dttm` COMMENT 'ETL process datetime'  ) 
    COMMENT 'Test_Table' 
   AS SELECT 
   `vender_no`,    -- vender number 
   `vender_nm`,    -- vender name 
   `acct_period`,    -- accounting period 
   `pur_qty`,    -- purchase quantity 
   `pur_avg_prc`,    -- purchase average price 
   `pur_amt`,    -- purchase amount 
   `src_db_nm`,    -- source database name 
   `src_tab_nm`,    -- source table name 
   `etl_job`,    -- ETL process job name 
   `etl_tx_dt`,    -- ETL extact date 
   `etl_upd_dt`,    -- ETL update date 
   `etl_proc_dttm`    -- ETL process datetime 
  FROM pt_dwd.test_table

/*=================================================*/
/* View: test_table_1 */
/* Definition: Test_Table_1 */
/*=================================================*/
CREATE OR REPLACE VIEW test_table_1 
    (`comp_no`  COMMENT 'company number' ,
  `acct_period`  COMMENT 'accounting period' ,
  `comp_nm`  COMMENT 'company name' ,
  `goods_no`  COMMENT 'goods number' ,
  `goods_nm`  COMMENT 'goods name' ,
  `goods_qty`  COMMENT 'goods quantity' ,
  `goods_desc`  COMMENT 'goods description' ,
  `buyer_no`  COMMENT 'buyer number' ,
  `buyer_nm`  COMMENT 'buyer name'  ) 
    COMMENT 'Test_Table_1' 
   AS SELECT 
   `comp_no`,    -- company number 
   `acct_period`,    -- accounting period 
   `comp_nm`,    -- company name 
   `goods_no`,    -- goods number 
   `goods_nm`,    -- goods name 
   `goods_qty`,    -- goods quantity 
   `goods_desc`,    -- goods description 
   `buyer_no`,    -- buyer number 
   `buyer_nm`    -- buyer name 
  FROM test_table_1

