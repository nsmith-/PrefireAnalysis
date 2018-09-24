import ROOT

fnum = ROOT.TFile.Open("prefiringJet_SingleMuon_Run2017F.root")
fdenom = ROOT.TFile.Open("prefiringJet_Run2017F.root")

tnum = fnum.Get("ntuple/tree")
tdenom = fdenom.Get("ntuple/tree")

tnum.Draw("jet_p4.Pt()*jet_neutralEmFrac:abs(jet_p4.Eta())>>hnum(5,2.5,3,20,0,400)", "Sum$(abs(jet_p4.Eta())>=2.)==1", "goff")
num = ROOT.gDirectory.Get("hnum")
tdenom.Draw("jet_p4.Pt()*jet_neutralEmFrac:abs(jet_p4.Eta())>>hdenom(5,2.5,3,20,0,400)", "Sum$(abs(jet_p4.Eta())>=2.)==1", "goff")
denom = ROOT.gDirectory.Get("hdenom")

num.Scale(1./num.Integral())
denom.Scale(1./denom.Integral())

num.Divide(denom)

# make coin-flip reweight more efficient
for iY in range(num.GetNbinsY()+1):
    maxbin = 0.
    for iX in range(num.GetNbinsX()+1):
        maxbin = max(maxbin, num.GetBinContent(iX, iY))
    if maxbin > 0.:
        for iX in range(num.GetNbinsX()+1):
            num.SetBinContent(iX, iY, num.GetBinContent(iX, iY)/maxbin)

num.Draw("colztext")
num.SetName("reweight")

fout = ROOT.TFile("reweight.root", "recreate")
num.Write()
