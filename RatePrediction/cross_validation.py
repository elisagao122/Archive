import re
import os.path

def stat_ida_before_date(date,dirpath, outpath):
    ida_dict = {}
    if os.path.isdir(dirpath):
        listfile = os.listdir(dirpath)
        for file in listfile:
            listdate = file.split('.')
            #print listdate
            if len(listdate) > 2 and listdate[2]<date:
                inputFile = os.path.join(dirpath,'access.log.'+listdate[2])
                outputFile = os.path.join(outpath,'ida_statistics_before_'+date)
                f = open(inputFile,'rb')
                file = open(outputFile,'w')
                for line in f.readlines():
                    m = re.match(r'^(.*)ida=(.{36})(.*)$',line)
                    if m:
                        if m.group(2) in ida_dict:
                            ida_dict[m.group(2)] = ida_dict[m.group(2)]+1
                        else:
                            ida_dict[m.group(2)] = 1
                f.close()
                for ida,value in ida_dict.iteritems():
                    file.write(ida+' = '+str(value)+'\n')
                file.close()

