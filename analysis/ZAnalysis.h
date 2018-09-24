//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Jun  7 12:16:34 2018 by ROOT version 6.12/06
// from TTree tree/Event Summary
// found on file: prefiringZ_Run2016H.root
//////////////////////////////////////////////////////////

#ifndef ZAnalysis_h
#define ZAnalysis_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TSelector.h>
#include <TTreeReader.h>
#include <TTreeReaderValue.h>
#include <TTreeReaderArray.h>
#include <TH2D.h>

// Headers needed by this particular selector
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/VectorUtil.h"

#include <vector>



class ZAnalysis : public TSelector {
public :
  typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> LorentzVector;
  TTreeReader    fReader;  //!the tree reader
  TTree       *fChain = 0;  //!pointer to the analyzed TTree or TChain

  // Readers to access the data (delete the ones you do not need).
  TTreeReaderValue<Long64_t> run = {fReader, "run"};
  TTreeReaderValue<Long64_t> lumi = {fReader, "lumi"};
  TTreeReaderValue<Long64_t> event = {fReader, "event"};
  TTreeReaderValue<Int_t> bunchCrossing = {fReader, "bunchCrossing"};
  TTreeReaderValue<Int_t> triggerRule = {fReader, "triggerRule"};
  TTreeReaderValue<LorentzVector> tag_electron = {fReader, "tag_electron"};
  TTreeReaderArray<LorentzVector> photon_p4 = {fReader, "photon_p4"};
  TTreeReaderArray<float> photon_sieie = {fReader, "photon_sieie"};
  TTreeReaderArray<float> photon_hoe = {fReader, "photon_hoe"};
  TTreeReaderArray<float> photon_iso = {fReader, "photon_iso"};
  TTreeReaderArray<int> L1EG_bx = {fReader, "L1EG_bx"};
  TTreeReaderArray<LorentzVector> L1EG_p4 = {fReader, "L1EG_p4"};
  TTreeReaderArray<int> L1EG_iso = {fReader, "L1EG_iso"};
  TTreeReaderArray<int> L1Jet_bx = {fReader, "L1Jet_bx"};
  TTreeReaderArray<LorentzVector> L1Jet_p4 = {fReader, "L1Jet_p4"};
  TTreeReaderArray<int> L1GtBx = {fReader, "L1GtBx"};


  ZAnalysis(TTree * /*tree*/ =0) { }
  virtual ~ZAnalysis() { }
  virtual Int_t  Version() const { return 2; }
  virtual void   Begin(TTree *tree);
  virtual void   SlaveBegin(TTree *tree);
  virtual void   Init(TTree *tree);
  virtual Bool_t  Notify();
  virtual Bool_t  Process(Long64_t entry);
  virtual Int_t  GetEntry(Long64_t entry, Int_t getall = 0) { return fChain ? fChain->GetTree()->GetEntry(entry, getall) : 0; }
  virtual void   SetOption(const char *option) { fOption = option; }
  virtual void   SetObject(TObject *obj) { fObject = obj; }
  virtual void   SetInputList(TList *input) { fInput = input; }
  virtual TList  *GetOutputList() const { return fOutput; }
  virtual void   SlaveTerminate();
  virtual void   Terminate();

  ClassDef(ZAnalysis,0);

private :
  TH2D * hEleL1EGmassL1Pt_bxm1_;
  TH2D * hEleL1EGmassL1Pt_bx0_;
  TH2D * hEleL1EGmassL1Pt_bx1_;

  TH2D * hEleL1EGEta2p0massL1Pt_bxm1_;
  TH2D * hEleL1EGEta2p0massL1Pt_bx0_;
  TH2D * hEleL1EGEta2p0massL1Pt_bx1_;

  TH2D * hEleL1EGEta2p5massL1Pt_bxm1_;
  TH2D * hEleL1EGEta2p5massL1Pt_bx0_;
  TH2D * hEleL1EGEta2p5massL1Pt_bx1_;

  TH2D * hElePhomass_PhoEta_;
  TH2D * hPhoIso_eta_mCut_;
  TH2D * hPhoSieie_eta_mCut_;
  TH2D * hPhoHoE_eta_mCut_;
  TH2D * hElePhoCutmass_PhoEta_;

  TH1D * hPhoL1EGDeltaR_bxm1_;
  TH1D * hPhoL1EGDeltaR_bx0_;
  TH1D * hPhoL1EGDeltaR_bx1_;
  TH1D * hPhoL1EGDeltaRsecond_;
  TH2D * hPhoL1EGnearestBx_;

  TH2D * hElePhomassPhoPt_bxm1_;
  TH2D * hElePhomassPhoPt_bx0_;
  TH2D * hElePhomassPhoPt_bx1_;

  TH2D * hElePhoEta1p0massPhoPt_bxm1_;
  TH2D * hElePhoEta1p0massPhoPt_bx0_;
  TH2D * hElePhoEta1p0massPhoPt_bx1_;

  TH2D * hElePhoEta2p0massPhoPt_bxm1_;
  TH2D * hElePhoEta2p0massPhoPt_bx0_;
  TH2D * hElePhoEta2p0massPhoPt_bx1_;

  TH2D * hElePhoEta2p5massPhoPt_bxm1_;
  TH2D * hElePhoEta2p5massPhoPt_bx0_;
  TH2D * hElePhoEta2p5massPhoPt_bx1_;

  template<typename T, typename... Args>
    T * newOutput(Args... args) {
      T * out = new T(args...);
      fOutput->Add(out);
      return out;
    };
};

#endif

#ifdef ZAnalysis_cxx
void ZAnalysis::Init(TTree *tree)
{
  // The Init() function is called when the selector needs to initialize
  // a new tree or chain. Typically here the reader is initialized.
  // It is normally not necessary to make changes to the generated
  // code, but the routine can be extended by the user if needed.
  // Init() will be called many times when running on PROOF
  // (once per file to be processed).

  fReader.SetTree(tree);
}

Bool_t ZAnalysis::Notify()
{
  // The Notify() function is called when a new file is opened. This
  // can be either for a new TTree in a TChain or when when a new TTree
  // is started when using PROOF. It is normally not necessary to make changes
  // to the generated code, but the routine can be extended by the
  // user if needed. The return value is currently not used.

  return kTRUE;
}


#endif // #ifdef ZAnalysis_cxx
