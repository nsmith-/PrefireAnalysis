import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import root_pandas

# To get:
# > brilcalc lumi -b "STABLE BEAMS" --normtag=/afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json \
# > -u /pb -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt --output-style csv > 2016lumi.csv
# Then change run:fill to run,fill
lumi = pd.read_csv("2016lumi.csv", comment='#')

def getds(name, fn):
    evts = root_pandas.read_root(fn, columns=["run", "lumi"])
    evts_run = evts.groupby("run").lumi.count().reset_index().rename(columns={'lumi':name})
    return evts_run


df = pd.merge(lumi, getds("muon", "prefiringJet_SingleMuon_Run2016B-H.root"), on="run")
df = pd.merge(df, getds("jet", "prefiringJet_JetHT_Run2016B-H.root"), on="run")

intlumi = df["recorded(/pb)"].cumsum() * 1.e-3

mratio = df["muon"]/df["recorded(/pb)"]
merr = np.sqrt(df["muon"])/df["recorded(/pb)"]

jratio = df["jet"]/df["recorded(/pb)"]
jerr = np.sqrt(df["jet"])/df["recorded(/pb)"]


plt.errorbar(intlumi, mratio, yerr=merr, fmt='.', label="SingleMuon")
plt.errorbar(intlumi, jratio, yerr=jerr, fmt='.', label="JetHT")
plt.xlabel("Integrated lumi (/fb)")
plt.ylabel("Unprefirable events * pb")
plt.yscale('log')
l = plt.legend()
l.set_title("2016 data")

mcorr = mratio.median()/mratio
jcorr = jratio.median()/jratio

# what a hack
import ROOT
fout = ROOT.TFile.Open("lumiCorrection.root", "recreate")
mcorr_table = ROOT.TGraph(len(mcorr), np.array(df["run"], dtype='d'), np.array(mcorr, dtype='d'))
mcorr_table.SetNameTitle("SingleMuon", "Lumi correction")
mcorr_table.Write()
jcorr_table = ROOT.TGraph(len(jcorr), np.array(df["run"], dtype='d'), np.array(jcorr, dtype='d'))
jcorr_table.SetNameTitle("JetHT", "Lumi correction")
jcorr_table.Write()
