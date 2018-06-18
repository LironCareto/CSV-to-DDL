# Based in code found in https://www.periscopedata.com/blog/python-create-table
import os, sys, csv, ast

table_name = os.path.splitext(sys.argv[1])[0] + '_' + os.path.splitext(sys.argv[1])[1][1:]

try:
    file_in = open(sys.argv[1])
    reader = csv.reader(file_in)
    longest, headers, type_list =  [], [], []

    def dataType(val, current_type):
        try:
            t = ast.literal_eval(val)
        except (ValueError, SyntaxError):
            return 'varchar'
        if (type(t) in ['int', 'long']) and current_type not in ['float', 'varchar']:
            #Use smallest int possible int type
            if (-32768 < t < 32767) and current not in ['bigint']:
                return 'smallint'
            elif (-2147483648 < t < 2147483647) and current_type not in ['bigint']:
                return 'int'
            else:
                return 'bigint'
        if type(t) is float and current_type not in ['varchar']:
            return 'decimal'
        else:
            return 'varchar'

    for row in reader:
        if len(headers) == 0:
            headers = row
            for col in row:
                longest.append(0)
                type_list.append('')
        else:
            for i in range(len(row)):
                if type_list[i] == 'varchar' or row[i] == 'NA':
                    pass
                else:
                    var_type = dataType(row[i], type_list[i])
                    type_list[i] = var_type
            if len(row[i]) > longest[i]:
                longest[i] > len(row[i])

finally:
    file_in.close()

sql_statement = 'create table ' + table_name + ' ('
for i in range(len(headers)):
    if type_list[i] == 'varchar':
        sql_statement = (sql_statement + '\n{} varchar({}),').format(headers[i].lower(),str(longest[i]))
    else:
        sql_statement = (sql_statement + '\n' + '{} {}' + ',').format(header[i].lower(),type_list[i])
sql_statement = sql_statement[:-1] + ');' + '\n' + '\n'
sql_statement = sql_statement + "load data infile '" + os.path.abspath(sys.argv[1]) + "' into table "+ table_name +" "\
"columns terminated by ';' "\
"ignore " + str(int(bool(len(headers)))) + " rows;"

try:
    file_out = open(table_name + '.sql','w')
    file_out.write(sql_statement)
finally:
    file_out.close()
