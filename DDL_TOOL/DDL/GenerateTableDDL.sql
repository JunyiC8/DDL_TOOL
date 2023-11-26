/*=================================================*/
/* Table: test_table */
/* Definition: Test_Table */
/*=================================================*/
DROP TABLE IF EXISTS pt_dwd.test_table;
CREATE TABLE pt_dwd.test_table 
    (`vender_no` BIGINT DEFAULT NULL COMMENT 'vender number' ,
  `vender_nm` VARCHAR(50) NOT NULL COMMENT 'vender name' ,
  `acct_period` VARCHAR(6) DEFAULT NULL COMMENT 'accounting period' ,
  `pur_qty` BIGINT NOT NULL COMMENT 'purchase quantity' ,
  `pur_avg_prc` Decimal(38,10) NOT NULL COMMENT 'purchase average price' ,
  `pur_amt` Decimal(38,10) NOT NULL COMMENT 'purchase amount' ,
  `src_db_nm` VARCHAR(50) NOT NULL COMMENT 'source database name' ,
  `src_tab_nm` VARCHAR(100) NOT NULL COMMENT 'source table name' ,
  `etl_job` VARCHAR(100) NOT NULL COMMENT 'ETL process job name' ,
  `etl_tx_dt` DATE NOT NULL COMMENT 'ETL extact date' ,
  `etl_upd_dt` DATE NOT NULL COMMENT 'ETL update date' ,
  `etl_proc_dttm` TIMESTAMP NOT NULL COMMENT 'ETL process datetime'  ) 
    COMMENT 'Test_Table' 
    CLUSTERED BY (vender_no,acct_period) 
        INTO 3 BUCKETS
   STORED AS ORC;

/*=================================================*/
/* Table: test_table_1 */
/* Definition: Test_Table_1 */
/*=================================================*/
DROP TABLE IF EXISTS test_table_1;
CREATE TABLE test_table_1 
    (`comp_no` BIGINT DEFAULT NULL COMMENT 'company number' ,
  `acct_period` VARCHAR(6) NOT NULL COMMENT 'accounting period' ,
  `comp_nm` VARCHAR(50) NOT NULL COMMENT 'company name' ,
  `goods_no` BIGINT DEFAULT NULL COMMENT 'goods number' ,
  `goods_nm` VARCHAR(50) NOT NULL COMMENT 'goods name' ,
  `goods_qty` BIGINT NOT NULL COMMENT 'goods quantity' ,
  `goods_desc` VARCHAR(200) NOT NULL COMMENT 'goods description' ,
  `buyer_no` BIGINT DEFAULT NULL COMMENT 'buyer number' ,
  `buyer_nm` VARCHAR(50) NOT NULL COMMENT 'buyer name'  ) 
    COMMENT 'Test_Table_1' 
PARTITIONED BY (fixed_dt DATE COMMENT 'fixed date')
   STORED AS ORC;

