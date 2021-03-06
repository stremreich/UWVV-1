from UWVV.AnalysisTools.AnalysisFlowBase import AnalysisFlowBase

import FWCore.ParameterSet.Config as cms


class MuonBaseFlow(AnalysisFlowBase):
    def __init__(self, *args, **kwargs):
        super(MuonBaseFlow, self).__init__(*args, **kwargs)

    def makeAnalysisStep(self, stepName, **inputs):
        step = super(MuonBaseFlow, self).makeAnalysisStep(stepName, **inputs)
        
        if stepName == 'preselection':
            self.addGhostCleaning(step)
            step.addBasicSelector('m', 'pt > 5 && (isGlobalMuon || isTrackerMuon)')
        elif stepName == 'embedding':
            self.addMuonPOGIDs(step)

        return step


    def addGhostCleaning(self, step):
        '''
        Add modules to resolve track ambiguities.
        '''
        mod = cms.EDProducer("PATMuonCleanerBySegments",
                             src = step.getObjTag('m'),
                             preselection = cms.string("track.isNonnull"),
                             passthrough = cms.string("isGlobalMuon && numberOfMatches >= 2"),
                             fractionOfSharedSegments = cms.double(0.499))

        step.addModule("muonGhostCleaning", mod, 'm')

    def addMuonPOGIDs(self, step):
        '''
        Add Muon POG IDs as UserInts

        '''
        embedMuId = cms.EDProducer(
                "MuonIdEmbedder",
                src = step.getObjTag('m'),
                vertexSrc = step.getObjTag('v')
            )
        step.addModule("muonIDembedding", embedMuId, 'm')

