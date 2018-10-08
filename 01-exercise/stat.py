import re, sys, operator
import codecs

f = codecs.open(sys.argv[1], 'r', errors='ignore')
#f = open('scorelib.txt', 'r', encoding="utf-8")

mode = sys.argv[2]
if mode == 'composer':
    pattern = re.compile(r"Composer: (.*)")
elif mode == 'century':
    #pattern = re.compile(r"Composition\s*Year:\s(\d{3,4}).*\n")
    pattern1 = re.compile(r"Composition\s*Year: .*(\d{4}).*\n")
    pattern2 = re.compile(r"Composition\s*Year: (\d+)\w+\s+century.*")
else:
    print("Wrong mode! Try again")
    sys.exit()

if mode == 'composer':
    result = re.findall(pattern, f.read())
    composers = []
    data = {}

    for i in result:
        if ';' in i:
            res = i.split(';')
            for c in res:
                composers.append(c.split('(')[0].strip())
        else:
            composers.append(i.split('(')[0].strip())

    for i in composers:
        if i in data:
            data.update({i: data[i] + 1})
        else:
            data.update({i: 1})

    for k, v in sorted(data.items(), key=lambda p: p[1], reverse=True):
        if (len(k) > 2):
            print('%s: %s' % (k, v))

else:
    result = re.findall(pattern2, f.read())
    f.seek(0)
    result.extend(re.findall(pattern1,f.read()))
    centuries = {}
    for i in result:
        if(len(i) < 3):
            century = i
            firstChars = str(int(century) -1)
        else:
            firstChars = i.strip()[:-2]
            century = str(int(firstChars) + 1) if i[-2:] != '00' else firstChars

        if str(int(firstChars) + 1) not in centuries:
            centuries.update({century.strip(): 1})
        else:
            centuries.update({century: centuries[century] + 1})

    for k, v in sorted(centuries.items(), key=lambda p: p[1], reverse=True):
        print('%s th century: %d' % (k, v))
