PrefireAnalysis
===============
This package helps analyze the effect of prefiring (particularly from EE in 2016-2017) on an analysis.
If interested in a full analysis, the installation and usage instructions are provided.
For a simple method to establish the impact of prefiring on an analysis, see the jet prefire efficiency map section.

Questions/comments: cms-l1t-ecal-prefiring@cern.ch

## Jet prefire efficiencies

For those who want a quick check, before diving deeper into the investigation, please consider the following method:

Rather than select the unprefirable subset of events in an analysis (which may often be too small to work with), one can attempt
to apply a localized prefire efficiency estimate on jets in the event, for those events where jets are the primary driver of the prefiring
inefficiency.  For example, in a VBF-like topology with two somewhat forward jets, one could imagine applying the following correction:
`sf = (1-eff(pt_j1, absEta_j1))*(1-eff(pt_j2, absEta_j2))` where the prefire efficiency is parameterized by the jet transverse momentum as well as its position in eta.  One could also try to isolate the effect by making an efficiency map as a function of jet EM pt (i.e. charged+neutral EM energy fraction * pt), and both types of parameterization have been investigated.  

_Preliminary_ maps of this efficiency are available for:
   - 2016 at https://ncsmith.web.cern.ch/ncsmith/PrefireEfficiencyMaps/
   - 2017 at https://lathomas.web.cern.ch/lathomas/TSGStuff/L1Prefiring/PrefiringMaps/
   
More information can be found in the presentations of https://indico.cern.ch/event/764279/#2-l1-pre-firing-in-2016-and-20

An overview/review of the effect can be found at https://indico.cern.ch/event/734407/contributions/3049707/

Questions/comments: cms-l1t-ecal-prefiring@cern.ch


## Installation
This should work in any `94X` CMSSW or newer
```bash
pushd $CMSSW_BASE/src
mkdir -p L1Trigger && cd L1Trigger
git clone git@github.com:nsmith-/PrefireAnalysis.git
cd ..
scram b
popd
```

## Usage
The idea is to select so-called 'unprefirable' events in whatever primary dataset is used for your analysis,
and then to check how often a (vetoed) L1A is present in the previous bunch crossing via the uGT record.

To select the events, the TCDS L1A history needs to be available.  It is found in AOD data as `L1AcceptBunchCrossingCollection`
with tag `scalersRawToDigi`, and an EDFilter is put in front of the analysis chain to read it: 
```python
process.prefireVetoFilter = cms.EDFilter("TriggerRulePrefireVetoFilter",
    l1AcceptRecordLabel = cms.InputTag("scalersRawToDigi"),
)

process.myPath = cms.Path(process.prefireVetoFilter + process.analysisChain)
```
If using MINIAOD, one can use the secondary file solution,
i.e. adding `secondaryFileNames` to `process.source`, or in the case of CRAB, `config.Data.useParent = True`.
A complete example that just saves the filtered MINIAOD events is in `test/testTriggerRulePrefireVeto_cfg.py`.

In your analysis chain, please save the uGT trigger decision (FinOR) of BX -1, accessed as follows:
```c++
#include "DataFormats/L1TGlobal/interface/GlobalAlgBlk.h"

// class MyAna : public edm::one::EDAnalyzer<edm::one::SharedResources> {
// ...
    edm::EDGetTokenT<BXVector<GlobalAlgBlk>> l1GtToken_;

// constructor...
  l1GtToken_(consumes<BXVector<GlobalAlgBlk>>(iConfig.getParameter<edm::InputTag>("l1GtSrc")))

// analyze function...
  edm::Handle<BXVector<GlobalAlgBlk>> l1GtHandle;
  iEvent.getByToken(l1GtToken_, l1GtHandle);
  bool prefire = l1GtHandle->begin(-1)->getFinalOR();
```
Then check with final selection how often this is true.  If the fraction is less than about 1%, then this means
there is no significant prefiring, as there is always the possibility (~L1A rate / MinBias rate) that interesting physics is
in the previous bunch crossing.  If much larger, then this is telling you the fraction of data in your phase
space lost due to prefiring.

## Event lists
Rather than run the unprefirable event filter (which requires AOD data tier), it may be simpler/faster to use event lists.
You will still need to save the trigger information from the previous bunch crossing, discussed below.
The following lists have been prepared:

| Primary Dataset | Unprefirable event count | ROOT file |
| --- | --- | --- |
| `JetHT/Run2017F-31Mar2018-v1` | 282287 | https://ncsmith.web.cern.ch/ncsmith/UnprefirableEventLists/JetHT_Run2017F_unprefirableEvents.root |
| `SingleElectron/Run2017F-31Mar2018-v1` | 143101 | https://ncsmith.web.cern.ch/ncsmith/UnprefirableEventLists/SingleElectron_Run2017F_unprefirableEvents.root |
| `SingleMuon/Run2017F-31Mar2018-v1` | 635747 | https://ncsmith.web.cern.ch/ncsmith/UnprefirableEventLists/SingleMuon_Run2017F_unprefirableEvents.root |
| `MET/Run2017F-31Mar2018-v1` | 367374 | https://ncsmith.web.cern.ch/ncsmith/UnprefirableEventLists/MET_Run2017F_unprefirableEvents.root |

Run2017 lists prepared with `Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt` lumimask.
Some events may be missing due to failed jobs, which is fine.
