import os, sys

sys.path.append(os.path.abspath(os.path.curdir))

if __name__ == '__main__':
    energies = [1,3,5,10,15,20,25,30] # List of energies of generated particles
    etaTags = ['1p7']                 # List of etas to shoot particles
    etas = {}
    etas['1p7'] = 1.7
    particles = [130]                 # List of particles to generate in pdg codes
    geometry = 'D41'                  # Geometry tag. Use >=D41
    cmssw = os.environ['CMSSW_VERSION']
    cmsswBase = os.environ['CMSSW_BASE']
    genDir = '%s/src/Configuration/GenProduction/python/'%cmsswBase
    unitsPerJob = 1
    njobs = 50
    cwd = os.getcwd()

    # Run cmsdriver.py to create workflows
    print('Creating step2 configuration.')
    os.system('cmsDriver.py step2 --conditions auto:phase2_realistic '
    '-s DIGI:pdigi_valid,L1,L1TrackTrigger,DIGI2RAW,HLT:@fake2 '
    '--datatier GEN-SIM-DIGI-RAW -n 100 --geometry Extended2023D41 '
    '--era Phase2C8_timing_layer_bar --eventcontent FEVTDEBUGHLT '
    '--filein file:step1.root --fileout file:step2.root'

    #os.system('sh createList.sh')
    #filein = open('myGeneration/list.txt','r')
    #nLine = 0

    for p in particles:
        for E in energies:
            for etaTag in etaTags:
                outTag = 'SingleK0L'
                outTag = '%s_E%d'%(outTag,E)
                outTag = '%sEta%s'%(outTag,etaTag)
                os.chdir(cwd)
		os.system('cp step2_DIGI_L1_L1TrackTrigger_DIGI2RAW_HLT.py myGeneration/%s/'%outTag)
		os.chdir('myGeneration/%s'%outTag)

                # Create CRAB configuration file
                file1 = open('crabConfig_%s.py'%outTag,'w')
                file1.write('# Script automatically generated using generator.py\n\n')
                file1.write('from CRABClient.UserUtilities ')
                file1.write('import config, getUsernameFromSiteDB\n')
                file1.write('config = config()\n')
                file1.write("config.General.requestName = ")
                file1.write("'%s_%s_upgrade2023_%s_step2'\n"%(outTag,cmssw,geometry))
                file1.write("config.General.workArea = 'crab_projects'\n")
                file1.write("config.General.transferOutputs = True\n")
                file1.write("config.General.transferLogs = True\n\n")
                file1.write("config.JobType.pluginName = 'Analysis'\n")
                file1.write("config.JobType.psetName = ")
                file1.write("'step2_DIGI_L1_L1TrackTrigger_DIGI2RAW_HLT.py'\n\n"%outTag)
                file1.write("config.Data.inputDataset = ''\n")#filein.readline(nLine)))
                file1.write("config.Data.inputDBS = 'phys03'\n")
		file1.write("config.Data.splitting = 'FileBased'\n")
                file1.write("config.Data.unitsPerJob = %d\n"%unitsPerJob)
                file1.write("config.Data.totalUnits = %d\n"%njobs)
                file1.write("config.Data.outLFNDirBase = '/store/user/%s/' ")
                file1.write("% (getUsernameFromSiteDB())\n")
                file1.write("config.Data.publication = True\n")
                file1.write("config.Data.outputDatasetTag = ")
                file1.write("'%s_%s_upgrade2023_%s_step2'\n\n"%(outTag,cmssw,geometry))
                file1.write("config.Site.storageSite = 'T3_US_FNALLPC'\n")
                file1.close()

                #os.system('crab submit -c crabConfig_%s.py'%outTag)
		#nLine = nLine + 1

os.system('rm step2_DIGI_L1_L1TrackTrigger_DIGI2RAW_HLT.py')