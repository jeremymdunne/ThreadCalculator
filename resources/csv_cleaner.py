# simple script to remove tabs from a file
# making this to clean some csv's I want to use

file = './unified_internal.dat'
out = './cleaned_unified_internal.dat'

with open(file,'r') as in_file:
    with open(out, 'w') as out_file:
        for line in in_file:
            for char in line:
                if(char != '\t'):
                    out_file.write(char)
    out_file.close()
    in_file.close()
