import re, sys, operator
import codecs

f = codecs.open(sys.argv[1], 'r', errors='ignore')
mode = sys.argv[2]

if mode == 'composer':
    pattern = re.compile(r"Composer: (.*)")
elif mode == 'centuries':
    pattern = re.compile(r"Composition\s*Year:\s(\d{3,4}).*\n")
else:
    print("Wrong mode! Try again")
    sys.exit()

result = re.findall(pattern, f.read())

if mode == 'composer':
    composers = []
    data = {}

    for i in result:
        if ';' in i:
            res = i.split(';')
            composers.extend(res)
        else:
            composers.append(i)

    for i in composers:
        if i in data:
            data.update({i: data[i] + 1})
        else:
            data.update({i: 1})

    for i in data:
        if len(i) < 2:
            continue
        print('%s: %s' % (i.lstrip().split('(')[0], data[i]))

else:
    centuries = {}
    for i in result:
        firstChars = i[:-2]
        century = str(int(firstChars) + 1) if i[-2:] != '00' else firstChars

        if str(int(firstChars) + 1) not in centuries:
            centuries.update({century: 1})
        else:
            centuries.update({century: centuries[century] + 1})

    sorted_centuries = sorted(centuries)

    for key in sorted_centuries:
        print('%s th century: %d' % (key, centuries[key]))
