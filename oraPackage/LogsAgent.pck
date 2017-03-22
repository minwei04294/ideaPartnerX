CREATE OR REPLACE PACKAGE LogsAgent
IS
-- 执行insert
procedure insert_region_log(p_dbid IN NUMBER);
--创建job
procedure create_job(p_dbid IN NUMBER,p_jobid OUT NUMBER);
-- 运行job
procedure run_job(p_dbid IN NUMBER);
-- 暂停job
procedure pause_job(p_dbid IN NUMBER);

END LogsAgent;
/
CREATE OR REPLACE PACKAGE BODY LogsAgent
IS
-- 执行insert
procedure insert_region_log(p_dbid IN NUMBER)
IS
   v_db_sql CLOB ;
   v_dblink_sql CLOB ;
   v_username varchar2(30) ;
   v_userpassw varchar2(30) ;
   v_server_ip varchar2(30) ;
   v_server_port varchar2(10) ;
   v_server_name varchar2(30) ;
   i NUMBER;
   v_dblink varchar2(30);
   BEGIN
   --创建dblink
     BEGIN
       v_db_sql := 'SELECT A.DB_USER_NAME,A.DB_USER_PASSWD,B.SERVER_IP,B.SERVER_PORT,B.SERVICE_NAME
       FROM DB_HUB A, DB_SERVER B
       WHERE A.SERVER_ID = B.SERVER_ID
       AND A.DB_ID = '||p_dbid;
       EXECUTE IMMEDIATE v_db_sql into v_username,v_userpassw,v_server_ip,v_server_port,v_server_name;
  
       EXECUTE IMMEDIATE 'SELECT COUNT(1) FROM User_Db_Links l where l.DB_LINK=UPPER('''||v_username||''')' into i;
       IF i =0 THEN
         v_dblink_sql := 'CREATE DATABASE LINK '||v_username||
         ' CONNECT TO '||v_username||
         ' IDENTIFIED BY "'||v_userpassw||
         '" using ''(DESCRIPTION = (ADDRESS_LIST = (ADDRESS = (PROTOCOL = TCP)(HOST = '||v_server_ip||' )(PORT = '||v_server_port||' )))(CONNECT_DATA = (SERVICE_NAME = '||v_server_name||' )))''';
         dbms_output.put_line(v_dblink_sql);
         EXECUTE IMMEDIATE v_dblink_sql;
       END IF;
       v_dblink := v_username;
     END;
     --执行insert
       FOR rec IN (SELECT 'INSERT INTO ' || N.TABLE_NAME || ' SELECT T.*,' || P_DBID ||
       ', SYSDATE, 0 FROM ' || N.TABLE_NAME || '@' || V_DBLINK ||
       ' T WHERE T.' || N.COLUMN_NAME || ' NOT IN (SELECT A.' ||
       N.COLUMN_NAME || ' FROM ' || N.TABLE_NAME || ' A)' AS MYSQL
  FROM (SELECT L.TABLE_NAME,
               L.CONSTRAINT_TYPE,
               C.COLUMN_NAME,
               ROW_NUMBER() OVER(PARTITION BY L.TABLE_NAME ORDER BY L.CONSTRAINT_TYPE) RN
          FROM USER_CONSTRAINTS L, USER_CONS_COLUMNS C
         WHERE L.TABLE_NAME IN ('LOG_ACTION',
                                'LOG_OPERATION',
                                'LOG_DETAIL',
                                'LOG_DETAIL_GRID')
           AND L.CONSTRAINT_TYPE IN ('P', 'R')
           AND L.CONSTRAINT_NAME = C.CONSTRAINT_NAME) N
 WHERE N.RN = 1) LOOP
         EXECUTE IMMEDIATE rec.mysql;
       END LOOP;
     COMMIT;
   END;
--创建job
procedure create_job(p_dbid IN NUMBER,p_jobid OUT NUMBER)
IS
  v_what varchar2(500) := 'declare dbid NUMBER(10) := '||p_dbid||';BEGIN LogsAgent.insert_region_log(dbid); END;';
  v_interval varchar2(200) := 'sysdate+1/(24*60)';
  BEGIN
    dbms_job.submit(
          job =>p_jobid, 
          what =>v_what, 
          next_date =>to_date('2017-01-01 08:00:00','yyyy-mm-dd hh24:mi:ss'), 
          interval =>v_interval);
    COMMIT;
  end;
-- 运行job
procedure run_job(p_dbid IN NUMBER)
IS
   v_jobid NUMBER;
   BEGIN
     SELECT L.JOB INTO v_jobid FROM USER_JOBS L WHERE REPLACE(REGEXP_SUBSTR(L.WHAT, '= [0-9]*'), '= ', '') = p_dbid;
     dbms_job.run(v_jobid);
     COMMIT;
   END;
-- 暂停job
procedure pause_job(p_dbid IN NUMBER)
IS
   v_jobid NUMBER;
   BEGIN
     SELECT L.JOB INTO v_jobid FROM USER_JOBS L WHERE REPLACE(REGEXP_SUBSTR(L.WHAT, '= [0-9]*'), '= ', '') = p_dbid;
     dbms_job.broken(v_jobid,TRUE);
     COMMIT;
   END;

END LogsAgent;
/
