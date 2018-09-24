#!/usr/bin/env python
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.workArea = 'crab_prefireJet'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'testPrefiringJet_cfg.py'

config.Data.splitting = 'FileBased'
# config.Data.splitting = 'Automatic'
config.Data.inputDBS = 'global'
config.Data.outLFNDirBase = '/store/user/%s/prefiringJet' % (getUsernameFromSiteDB())
config.Data.publication = False
#config.Data.allowNonValidInputDataset = True
config.Data.unitsPerJob = 1
#config.JobType.numCores = 4
config.Data.useParent = True

config.Site.storageSite = 'T2_US_Wisconsin'
#config.Site.storageSite = 'T2_CH_CERN'

pds = [
    '/JetHT/Run2016B-03Feb2017_ver2-v2/MINIAOD',
    '/JetHT/Run2016C-03Feb2017-v1/MINIAOD',
    '/JetHT/Run2016D-03Feb2017-v1/MINIAOD',
    '/JetHT/Run2016E-03Feb2017-v1/MINIAOD',
    '/JetHT/Run2016F-03Feb2017-v1/MINIAOD',
    '/JetHT/Run2016G-03Feb2017-v1/MINIAOD',
    '/JetHT/Run2016H-03Feb2017_ver2-v1/MINIAOD',
    '/JetHT/Run2016H-03Feb2017_ver3-v1/MINIAOD',
    '/JetHT/Run2017B-31Mar2018-v1/MINIAOD',
    '/JetHT/Run2017F-31Mar2018-v1/MINIAOD',
    '/MET/Run2017F-31Mar2018-v1/MINIAOD',
    '/SingleMuon/Run2016H-03Feb2017_ver2-v1/MINIAOD',
    '/SingleMuon/Run2017F-31Mar2018-v1/MINIAOD',
]

if __name__ == '__main__':
    from CRABAPI.RawCommand import crabCommand
    from CRABClient.ClientExceptions import ClientException
    from httplib import HTTPException

    def submit(config):
        try:
            crabCommand('submit', config = config)
        except HTTPException as hte:
            print "Failed submitting task: %s" % (hte.headers)
        except ClientException as cle:
            print "Failed submitting task: %s" % (cle)

    for i, pd in enumerate(pds):
        (_, primaryDS, conditions, dataTier) = pd.split('/')
        config.General.requestName = 'prefiringJet_%s_%s' % (primaryDS, conditions)
        config.Data.outputDatasetTag = conditions
        config.Data.inputDataset = pd
        if 'Run2017' in conditions:
            config.Data.lumiMask ='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'
            config.JobType.pyCfgParams = ['is2016=0']
        elif 'Run2016' in conditions:
            config.Data.lumiMask ='/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt'
            config.JobType.pyCfgParams = ['is2016=1']
        submit(config)
