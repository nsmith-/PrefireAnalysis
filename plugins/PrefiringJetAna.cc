// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/transform.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "PhysicsTools/SelectorUtils/interface/PFJetIDSelectionFunctor.h"
#include "DataFormats/L1Trigger/interface/EGamma.h"
#include "DataFormats/L1Trigger/interface/Jet.h"
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"
#include "DataFormats/PatCandidates/interface/TriggerObjectStandAlone.h"
#include "DataFormats/PatCandidates/interface/PackedTriggerPrescales.h"
#include "DataFormats/HLTReco/interface/TriggerTypeDefs.h"

#include "TTree.h"

#include "Math/LorentzVector.h"
#include "Math/PxPyPzE4D.h"
// == reco::LorentzVector
typedef ROOT::Math::LorentzVector<ROOT::Math::PxPyPzE4D<double>> LorentzVector;

namespace {
  struct EventStruct {
    Long64_t run;
    Long64_t lumi;
    Long64_t event;
    int bunchCrossing;
    int triggerRule;
    
    std::vector<LorentzVector> jet_p4;
    std::vector<float> jet_neutralEmFrac;
    std::vector<float> jet_neutralHadFrac;
    std::vector<float> jet_muonFrac;
    // bits 0=loose ID, 1=tight ID, 2-4=match to HLT_PFJet 450,500,550
    std::vector<int> jet_id;

    LorentzVector met;

    std::vector<int> L1EG_bx;
    std::vector<LorentzVector> L1EG_p4;
    std::vector<int> L1EG_iso;

    std::vector<int> L1Jet_bx;
    std::vector<LorentzVector> L1Jet_p4;

    std::vector<int> L1GtBx;
  };

  std::vector<const pat::TriggerObjectStandAlone*> getMatchedObjs(const float eta, const float phi, const std::vector<pat::TriggerObjectStandAlone>& trigObjs, const float maxDeltaR=0.1)
  {
    std::vector<const pat::TriggerObjectStandAlone*> matchedObjs;
    const float maxDR2 = maxDeltaR*maxDeltaR;
    for(auto& trigObj : trigObjs){
      const float dR2 = reco::deltaR2(eta,phi,trigObj.eta(),trigObj.phi());
      if(dR2<maxDR2) matchedObjs.push_back(&trigObj);
    }
    return matchedObjs;
  }
}

class PrefiringJetAna : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
  public:
    explicit PrefiringJetAna(const edm::ParameterSet&);
    ~PrefiringJetAna();

    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

  private:
    // virtual void beginJob() override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    // virtual void endJob() override;

    PFJetIDSelectionFunctor looseJetIdSelector_{PFJetIDSelectionFunctor::WINTER16, PFJetIDSelectionFunctor::LOOSE};
    pat::strbitset hasLooseId_;
    PFJetIDSelectionFunctor tightJetIdSelector_{PFJetIDSelectionFunctor::WINTER16, PFJetIDSelectionFunctor::TIGHT};
    pat::strbitset hasTightId_;

    edm::EDGetTokenT<int> triggerRuleToken_;
    edm::EDGetTokenT<pat::JetCollection> jetToken_;
    edm::EDGetTokenT<pat::METCollection> metToken_;
    StringCutObjectSelector<pat::Jet> tagJetCut_;
    edm::EDGetTokenT<BXVector<l1t::EGamma>> l1egToken_;
    edm::EDGetTokenT<BXVector<l1t::Jet>> l1jetToken_;
    edm::EDGetTokenT<BXVector<GlobalAlgBlk>> l1GtToken_;
    edm::EDGetTokenT<pat::TriggerObjectStandAloneCollection> triggerObjectsToken_;
    edm::EDGetTokenT<pat::PackedTriggerPrescales> triggerPrescalesToken_;

    TTree * tree_;
    EventStruct event_;
};

PrefiringJetAna::PrefiringJetAna(const edm::ParameterSet& iConfig):
  triggerRuleToken_(consumes<int>(iConfig.getParameter<edm::InputTag>("triggerRule"))),
  jetToken_(consumes<pat::JetCollection>(iConfig.getParameter<edm::InputTag>("jetSrc"))),
  metToken_(consumes<pat::METCollection>(iConfig.getParameter<edm::InputTag>("metSrc"))),
  tagJetCut_(iConfig.getParameter<std::string>("tagJetCut")),
  l1egToken_(consumes<BXVector<l1t::EGamma>>(iConfig.getParameter<edm::InputTag>("l1egSrc"))),
  l1jetToken_(consumes<BXVector<l1t::Jet>>(iConfig.getParameter<edm::InputTag>("l1jetSrc"))),
  l1GtToken_(consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("l1GtSrc"))),
  triggerObjectsToken_(consumes<pat::TriggerObjectStandAloneCollection>(iConfig.getParameter<edm::InputTag>("triggerObjects"))),
  triggerPrescalesToken_(consumes<pat::PackedTriggerPrescales>(iConfig.getParameter<edm::InputTag>("triggerPrescales")))
{
  usesResource("TFileService");
  edm::Service<TFileService> fs;

  hasLooseId_ = looseJetIdSelector_.getBitTemplate();
  hasTightId_ = tightJetIdSelector_.getBitTemplate();

  tree_ = fs->make<TTree>("tree","Event Summary");
  tree_->Branch("run", &event_.run);
  tree_->Branch("lumi", &event_.lumi);
  tree_->Branch("event", &event_.event);
  tree_->Branch("bunchCrossing", &event_.bunchCrossing);
  tree_->Branch("triggerRule", &event_.triggerRule);
  tree_->Branch("jet_p4", &event_.jet_p4);
  tree_->Branch("jet_neutralEmFrac", &event_.jet_neutralEmFrac);
  tree_->Branch("jet_neutralHadFrac", &event_.jet_neutralHadFrac);
  tree_->Branch("jet_muonFrac", &event_.jet_muonFrac);
  tree_->Branch("jet_id", &event_.jet_id);
  tree_->Branch("met", &event_.met);
  tree_->Branch("L1EG_bx", &event_.L1EG_bx);
  tree_->Branch("L1EG_p4", &event_.L1EG_p4);
  tree_->Branch("L1EG_iso", &event_.L1EG_iso);
  tree_->Branch("L1Jet_bx", &event_.L1Jet_bx);
  tree_->Branch("L1Jet_p4", &event_.L1Jet_p4);
  tree_->Branch("L1GtBx", &event_.L1GtBx);
}


PrefiringJetAna::~PrefiringJetAna()
{
}

void
PrefiringJetAna::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace edm;

  event_.run = iEvent.run();
  event_.lumi = iEvent.luminosityBlock();
  event_.event = iEvent.id().event();
  event_.bunchCrossing = iEvent.bunchCrossing();

  Handle<int> triggerRuleHandle;
  iEvent.getByToken(triggerRuleToken_, triggerRuleHandle);
  event_.triggerRule = *triggerRuleHandle;

  Handle<pat::JetCollection> jetHandle;
  iEvent.getByToken(jetToken_, jetHandle);

  Handle<pat::METCollection> metHandle;
  iEvent.getByToken(metToken_, metHandle);

  Handle<BXVector<l1t::EGamma>> l1egHandle;
  iEvent.getByToken(l1egToken_, l1egHandle);

  Handle<BXVector<l1t::Jet>> l1jetHandle;
  iEvent.getByToken(l1jetToken_, l1jetHandle);

  Handle<BXVector<GlobalAlgBlk>> l1GtHandle;
  iEvent.getByToken(l1GtToken_, l1GtHandle);

  Handle<pat::TriggerObjectStandAloneCollection> triggerObjectsHandle;
  iEvent.getByToken(triggerObjectsToken_, triggerObjectsHandle);

  Handle<pat::PackedTriggerPrescales> triggerPrescalesHandle;
  iEvent.getByToken(triggerPrescalesToken_, triggerPrescalesHandle);
  const edm::TriggerResults& triggerResults = triggerPrescalesHandle->triggerResults();


  event_.jet_p4.clear();
  event_.jet_neutralEmFrac.clear();
  event_.jet_neutralHadFrac.clear();
  event_.jet_muonFrac.clear();
  event_.jet_id.clear();
  for(const auto& jet : *jetHandle) {
    pat::Jet jetNew(jet);
    int packedIds = 0;
    jetNew.addUserInt("looseJetId", looseJetIdSelector_(jetNew, hasLooseId_));
    packedIds |= ((int) looseJetIdSelector_(jetNew, hasLooseId_))<<0;
    jetNew.addUserInt("tightJetId", tightJetIdSelector_(jetNew, hasTightId_));
    packedIds |= ((int) tightJetIdSelector_(jetNew, hasTightId_))<<1;

    if ( not tagJetCut_(jetNew) ) continue;

    std::vector<const pat::TriggerObjectStandAlone*> matchedTrigObjs = getMatchedObjs(jet.eta(), jet.phi(), *triggerObjectsHandle, 0.3);
    for (const auto trigObjConst : matchedTrigObjs) {
      pat::TriggerObjectStandAlone trigObj(*trigObjConst);
      trigObj.unpackNamesAndLabels(iEvent, triggerResults);

      // HLT_PFJetX_v*
      if ( trigObj.hasFilterLabel("hltSinglePFJet450") ) {
        packedIds |= 1<<2;
      }
      if ( trigObj.hasFilterLabel("hltSinglePFJet500") ) {
        packedIds |= 1<<3;
      }
      if ( trigObj.hasFilterLabel("hltSinglePFJet550") ) {
        packedIds |= 1<<4;
      }
    }

    event_.jet_p4.push_back( jetNew.p4() );
    event_.jet_neutralEmFrac.push_back( jetNew.neutralEmEnergyFraction() );
    event_.jet_neutralHadFrac.push_back( jetNew.neutralHadronEnergyFraction() );
    event_.jet_muonFrac.push_back( jetNew.muonEnergyFraction() );
    event_.jet_id.push_back( packedIds );
  }

  event_.met = metHandle->at(0).p4();

  event_.L1EG_bx.clear();
  event_.L1EG_p4.clear();
  event_.L1EG_iso.clear();
  for (auto bx=l1egHandle->getFirstBX(); bx<l1egHandle->getLastBX()+1; ++bx) {
    for (auto itL1=l1egHandle->begin(bx); itL1!=l1egHandle->end(bx); ++itL1) {
      event_.L1EG_bx.push_back(bx);
      event_.L1EG_p4.push_back(itL1->p4());
      event_.L1EG_iso.push_back(itL1->hwIso());
    }
  }

  event_.L1Jet_bx.clear();
  event_.L1Jet_p4.clear();
  for (auto bx=l1jetHandle->getFirstBX(); bx<l1jetHandle->getLastBX()+1; ++bx) {
    for (auto itL1=l1jetHandle->begin(bx); itL1!=l1jetHandle->end(bx); ++itL1) {
      event_.L1Jet_bx.push_back(bx);
      event_.L1Jet_p4.push_back(itL1->p4());
    }
  }

  event_.L1GtBx.clear();
  for (auto bx=l1GtHandle->getFirstBX(); bx<l1GtHandle->getLastBX()+1; ++bx) {
    event_.L1GtBx.push_back(l1GtHandle->begin(bx)->getFinalOR());
  }

  tree_->Fill();
}


void
PrefiringJetAna::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}


DEFINE_FWK_MODULE(PrefiringJetAna);
