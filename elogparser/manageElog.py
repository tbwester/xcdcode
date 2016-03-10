out = open('output.txt-1', 'w')
with open("runlistCampaign4-1.txt") as f:
    for line in f:
        if "Run#" in line:
            out.write(line[5:].strip())
            out.write('|')
        if "RunFileName" in line:
            out.write(line[12:].strip())
            out.write('|')
        if "Run Type" in line:
            out.write(line[9:].strip())
            out.write('|')
        if "Source" in line:
            out.write(line[7:].strip())
            out.write('|')
        if "Capacitor" in line:
            out.write(line[10:].strip())
            out.write('\n')
        if "PMT HV" in line:
            out.write(line[7:].strip())
            out.write('|')
        if "Events#" in line:
            out.write(line[8:].strip())
            out.write('|')
        if "Start Time" in line:
            out.write(line[11:].strip())
            out.write('|')
        if "Trigger Rate" in line:
            out.write(line[13:].strip())
            out.write('|')
        if "Pre-Trigger" in line:
            out.write(line[12:].strip())
            out.write('|')
        if "Total gate" in line:
            out.write(line[11:].strip())
            out.write('|')
        if "Digitizer Trigger" in line:
            out.write(line[18:].strip())
            out.write('|')
        
        
out.close()
