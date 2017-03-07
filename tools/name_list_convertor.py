out = open('out.names', 'w')

names = []
current = []
count = 0

start_set = 'set(['
end_set = ']) | '

for line in [line.strip(' \t\n\r') for line in open('Persian_Names_(2).csv')]:
    for word in [word.strip(' \t\n\r"') for word in line.split(',')]:
        if word != '':
            if count == 255:
                count = 0
                out.write(', '.join(current))
                current = []
                out.write(end_set)
            if count == 0:
                out.write(start_set)
            count += 1
            current.append('"' + word.lower() + '"')

if count != 0:
    out.write(', '.join(current))
    out.write('])')

