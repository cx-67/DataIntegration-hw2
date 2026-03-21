import pymysql
import os

# 本地数据库配置
LOCAL_HOST = 'BPeril'
LOCAL_PORT = 3306
LOCAL_USER = 'datax'
LOCAL_PWD  = 'DxPwd123!'
LOCAL_DB   = 'DIDatax'

# SQL 文件路径
SQL_FILE = os.path.join(os.path.dirname(__file__), '..', 'sql', 'create_tables.sql')

def run_sql_file():
    print(f"Connecting to {LOCAL_HOST}:{LOCAL_PORT}/{LOCAL_DB} as {LOCAL_USER}...")
    try:
        conn = pymysql.connect(
            host=LOCAL_HOST,
            port=LOCAL_PORT,
            user=LOCAL_USER,
            password=LOCAL_PWD,
            database=LOCAL_DB,
            charset='utf8mb4'
        )
        cursor = conn.cursor()
        
        print(f"Reading SQL file: {SQL_FILE}")
        with open(SQL_FILE, 'r', encoding='utf-8') as f:
            sql_content = f.read()
            
        # 简单分割 SQL 语句（以分号分割）
        statements = sql_content.split(';')
        
        for statement in statements:
            statement = statement.strip()
            if statement and not statement.startswith('--'):
                try:
                    # 打印当前执行的语句摘要
                    table_name_match = statement.upper().find('CREATE TABLE IF NOT EXISTS')
                    if table_name_match != -1:
                        table_name = statement[table_name_match:].split()[5] # 大致获取表名
                        print(f"Creating table: {table_name}...")
                    
                    cursor.execute(statement)
                except Exception as e:
                    print(f"Error executing statement: {e}")
                    # 不阻断后续表创建
        
        print("Committing changes...")
        conn.commit()
        print("Verified tables created:")
        cursor.execute("SHOW TABLES")
        for (table_name,) in cursor:
            print(f" - {table_name}")
            
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        if 'conn' in locals() and conn.open:
            cursor.close()
            conn.close()
            print("Connection closed.")

if __name__ == '__main__':
    run_sql_file()
