#!/usr/bin/python

# This script appends utterances dumped out from XML to a Kaldi datadir

import sys, re

basename=sys.argv[1]
outdir = sys.argv[2]

if len(sys.argv) > 3 and sys.argv[3]!="all" :
    pmer_thresh=float(sys.argv[3])
else:
    pmer_thresh = None

# open the output files in append mode
segments_file = open(outdir + '/segments', 'a')
utt2spk_file = open(outdir + '/utt2spk', 'a')
text_file = open(outdir + '/text', 'a')

for line in sys.stdin:

    m = re.match(r'\w+speaker(\d+)\w+\s+(.*)', line)

    if m:

        spk = int(m.group(1))

        t = m.group(2).split()
        start = float(t[0])
        end = float(t[1])
        mer = float(t[2])
        words = ' '.join(t[5:])
	pmer = float(t[3])
	awd = float(t[4])

        segId = '%s_spk-%04d_seg-%07d:%07d' % (basename, spk, start*100, end*100)
        spkId = '%s_spk-%04d' % (basename, spk)

        # only add segments where the Matching Error Rate is below the prescribed threshhold
        if (pmer_thresh == None or pmer <= pmer_thresh) and awd >= 0.165 and awd <= 0.66:
            print >> segments_file, '%s %s %.2f %.2f' % (segId, basename, start, end ) 
            print >> text_file, '%s %s' % (segId, words)
            print >> utt2spk_file, '%s %s' % (segId, spkId)
# test
segments_file.close()
utt2spk_file.close()
text_file.close()
 
            
