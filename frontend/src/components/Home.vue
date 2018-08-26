<template>
    <div class="row">
        <div class="col-4 d-flex flex-wrap">
            <common-turn-off-all  class="w-50 mt-3 px-2"></common-turn-off-all>
            <common-select-only-audio class="w-50 mt-3 px-2"></common-select-only-audio>
            <common-select-central-apple-tv class="w-50 mt-3 px-2"></common-select-central-apple-tv>
            <common-select-single-apple-tv class="w-50 mt-3 px-2"></common-select-single-apple-tv>
            <common-select-mobile-transmitter class="w-50 mt-3 px-2"></common-select-mobile-transmitter>
        </div>
        <div class="col-4 d-flex flex-wrap">
            <single-volume-down :projector-id="2" class="w-50 mt-3 px-2"></single-volume-down>
            <single-volume-up :projector-id="2" class="w-50 mt-3 px-2"></single-volume-up>
            <single-mute :projector-id="2" class="w-50 mt-3 px-2"></single-mute>
            <common-freeze :projector-id="2" class="w-50 mt-3 px-2"></common-freeze>
            <common-blank :projector-id="2" class="w-50 mt-3 px-2"></common-blank>
        </div>
        <div class="col-4 d-flex flex-wrap">
            <projector-state-small :projector-id="1" class="w-100 mt-3"></projector-state-small> 
            <projector-state-small :projector-id="2" class="w-100 mt-2"></projector-state-small>    
            <projector-state-small :projector-id="3" class="w-100 mt-2"></projector-state-small>
            <button-box text="Luci Sala" class="w-100 mt-2"></button-box>
            <!-- <div class="card w-100 mt-3 elegant-color">
                <div class="card-body">
                    Audio Sala
                </div>
            </div> -->
        </div>
    </div>
</template>

<script>
import ProjectorStateSmall from './ProjectorStateSmall.vue'
import ButtonBox from './ButtonBox.vue'
import CommonTurnOffAll from './Buttons/CommonTurnOffAll.vue'
import CommonSelectCentralAppleTv from './Buttons/CommonSelectCentralAppleTv.vue'
import CommonSelectSingleAppleTv from './Buttons/CommonSelectSingleAppleTv.vue'
import CommonSelectMobileTransmitter from './Buttons/CommonSelectMobileTransmitter.vue'
import CommonSelectOnlyAudio from './Buttons/CommonSelectOnlyAudio.vue'
import SingleVolumeUp from './Buttons/SingleVolumeUp.vue'
import SingleVolumeDown from './Buttons/SingleVolumeDown.vue'
import SingleMute from './Buttons/SingleMute.vue'
import CommonFreeze from './Buttons/CommonFreeze.vue'
import CommonBlank from './Buttons/CommonBlank.vue'

export default {
    name: "home",
    components: {
        ProjectorStateSmall,
        ButtonBox,
        CommonTurnOffAll,
        CommonSelectCentralAppleTv,
        CommonSelectSingleAppleTv,
        CommonSelectMobileTransmitter,
        CommonSelectOnlyAudio,
        SingleVolumeUp,
        SingleVolumeDown,
        SingleMute,
        CommonFreeze,
        CommonBlank
    }
}
</script>

<style lang="sass" scoped>

</style>