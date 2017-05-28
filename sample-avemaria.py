# -*- coding:utf-8 -*-

from ymz294lib import ymz294
from ymz294lib import sequencer

#set GPIO number connecting to D0 ~ D7 pin
dpins = (17,27,22,10,9,11,5,6)
psg = ymz294.PSGPlayer(dpins, 18, 18, 24)

#ChA vol=Envelop, ChB vol=15, ChC vol=11
psg.setVolume(ymz294.PSGPlayer.CHANNEL_A, 9, True)
psg.setVolume(ymz294.PSGPlayer.CHANNEL_B, 15, False)
psg.setVolume(ymz294.PSGPlayer.CHANNEL_C, 11, False)

#Envelop Frequency=1.2Hz, Type=9
psg.setEnvelopFreq(1.2)
psg.setEnvelopType(9)

#ChA:melody=on, noise=off 
#ChB:melody=on, noise=off
#ChC melody=off, noise=off
psg.setMixer(True, False, True, False, False, False)

#set noise frequency (C.O.)
#psg.setNoise(8000)

player = sequencer.Sequencer(psg)

# MML string
mmlA_1 = "T80O4L16CEG>CE<G>CE<CEG>CE<G>CE <CDA>DF<A>DF<CDA>DF<A>DF <<B>DG>DF<G>DF<<B>DG>DF<G>DF <CEG>CE<G>CE<CEG>CE<G>CE"
mmlB_1 = "T80O4L8R1R1R1R1"
mmlA_2 = mmlA_1
mmlB_2 = "T80O4L8E1F2.RFG2.D4E2&ERR4"
mmlA_3 = "T80O4L16CE>CEACEA<CE>CEACEA <CDF+A>D<F+A>D<CDF+A>D<F+A>D <<B>DG>DG<G>DG<<B>DG>DG<G>DG <<B>CEG>C<EG>C<<B>CEG>C<EG>C"
mmlB_3 = "T80O4L8A2&A<AB>CD4.ED4R4G2&G<GAB>C4.DC4R4"

# play
corefreq = 466 #466Hz is Chorton pitch. Normally (and if you emitted) 440Hz
player.playMML(mmlA_1, mmlB_1, core_freq=corefreq)
player.playMML(mmlA_2, mmlB_2, core_freq=corefreq)
player.playMML(mmlA_3, mmlB_3, core_freq=corefreq)

# mute
psg.setVolume(ymz294.PSGPlayer.CHANNEL_A, 0)
psg.setVolume(ymz294.PSGPlayer.CHANNEL_B, 0)
psg.setVolume(ymz294.PSGPlayer.CHANNEL_C, 0)


