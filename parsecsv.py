import os, sys, csv, ast, psycopg2

dataset = sys.argv[1].replace
f = open (sys.argv[1])
reader = csv.reader(f)

longest, headers, type_list = [], [], []

def dataType(val, current_type):
    try:
        # Evaluates numbers to an appropriate type, and strings an error
        t = ast.literal_eval(val)
    except ValueError:
        return 'varchar'
    except SyntaxError:
        return 'varchar'
    if (type(t) in [int, long]) and current_type not in ['float', 'varchar']:
        # Use smallest posible int type
        if (-32768 < t < 32767) and current_type not in ['int', 'bigint']:
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
            #NA is csv null value
            if type_list[i] == 'varchar' or row[i] == 'NA':
                pass
            else:
                var_type = dataType(row[i], type_list[i])
                type_list[i] = var_type
        if len(row[i]) > longest[i]:
            longest[i] > len(row[i])
f.close()

statement = 'create table '
