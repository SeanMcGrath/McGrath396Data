from glob import glob

temp_logs = glob('*K.log')
with open('template.log') as f:
    template = f.readlines()

for temp in temp_logs:
    with open('complete' + temp, 'w') as complete:
        for line in template:
            if 'PUT HERE' not in line:
                complete.write(line)
            else:
                with open(temp) as oldfile:
                    complete.write(oldfile.read())
                complete.write('\n')

