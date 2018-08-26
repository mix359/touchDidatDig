<template>
    <div class="row">
        <div class="col-4 d-flex flex-wrap">
            <div class="card indigo darken-1 ripple-parent w-100 mt-3">
                <div class="card-body">
                    <h4>Proiettore {{projector.name}}</h4>
                    
                    <div>Sorgente: {{source}}</div>
                    <div>Muto: {{projector.muted ? 'Si' : 'No'}} <i class="fa fa-volume-off ml-2" v-if="projector.muted"></i></div>
                    <div>Congelato: {{projector.freezed ? 'Si' : 'No'}} <i class="fa fa-snowflake-o ml-2" v-if="projector.freezed"></i> </div>
                    <div>Oscurato: {{projector.blanked ? 'Si' : 'No'}} <i class="fa fa-square-o ml-2" v-if="projector.blanked"></i></div>

                    <div>Volume:</div>
                    <div class="progress md-progress" style="height: 20px">
                        <div class="progress-bar" role="progressbar" style="height: 20px" :style="'width: ' + volume + '%;'" :aria-valuenow="volume" aria-valuemin="0" aria-valuemax="100">{{volume}}%</div>
                    </div>
                </div>
            </div>
            <button-box text="Home" class="w-100 mt-3" @click="$store.commit('changePage', 0)"></button-box>
        </div>
        <div class="col-4 d-flex flex-wrap">
            <single-turn-off :projector-id="projectorId" class="w-50 mt-3 px-2"></single-turn-off>
            <single-select-apple-tv :projector-id="projectorId" class="w-50 mt-3 px-2"></single-select-apple-tv>
            <single-select-central-apple-tv :projector-id="projectorId" class="w-50 mt-3 px-2"></single-select-central-apple-tv>
            <single-select-mobile-transmitter :projector-id="projectorId" class="w-50 mt-3 px-2"></single-select-mobile-transmitter>
            <single-select-vga :projector-id="projectorId" class="w-50 mt-3 px-2"></single-select-vga>
        </div>
        <div class="col-4 d-flex flex-wrap">
            <single-volume-down :projector-id="projectorId" class="w-50 mt-3 px-2"></single-volume-down>
            <single-volume-up :projector-id="projectorId" class="w-50 mt-3 px-2"></single-volume-up>
            <single-mute :projector-id="projectorId" class="w-50 mt-3 px-2"></single-mute>
            <single-freeze :projector-id="projectorId" class="w-50 mt-3 px-2"></single-freeze>
            <single-blank :projector-id="projectorId" class="w-50 mt-3 px-2"></single-blank>
        </div>
    </div>
</template>

<script>
import ButtonBox from './ButtonBox.vue'
import SingleTurnOff from './Buttons/SingleTurnOff.vue'
import SingleSelectCentralAppleTv from './Buttons/SingleSelectCentralAppleTv.vue'
import SingleSelectAppleTv from './Buttons/SingleSelectAppleTv.vue'
import SingleSelectMobileTransmitter from './Buttons/SingleSelectMobileTransmitter.vue'
import SingleSelectVga from './Buttons/SingleSelectVga.vue'
import SingleVolumeUp from './Buttons/SingleVolumeUp.vue'
import SingleVolumeDown from './Buttons/SingleVolumeDown.vue'
import SingleMute from './Buttons/SingleMute.vue'
import SingleFreeze from './Buttons/SingleFreeze.vue'
import SingleBlank from './Buttons/SingleBlank.vue'

export default {
    name: "projector",
    props: {
        projectorId: {required: true, type: Number}
    },
    components: {
        ButtonBox,
        SingleTurnOff,
        SingleSelectCentralAppleTv,
        SingleSelectAppleTv,
        SingleSelectMobileTransmitter,
        SingleSelectVga,
        SingleVolumeUp,
        SingleVolumeDown,
        SingleMute,
        SingleFreeze,
        SingleBlank
    },
    computed: {
        projector() {
            return this.$store.state.projectors[this.projectorId];
        },
        videoMatrix() {
            return this.$store.state.videoMatrixes[this.projectorId];
        },
        volume() {
            return this.projector.vol;
        },
        source() {
            if(!this.projector.powered) {
                return "Spento";
            }

            if(this.projector.source === this.$definitions.PROJECTOR_SOURCE_VGA) {
                return "VGA";
            }

            if(this.projector.source === this.$definitions.PROJECTOR_SOURCE_HDMI1) {
                return "Apple Tv";
            }

            if(this.projector.source === this.$definitions.PROJECTOR_SOURCE_HDMI2 && 
            this.videoMatrix.channel === this.$definitions.VIDEO_MATRIX_CHANNEL_APPLE_TV) {
                return "Apple Tv Centrale";
            }

            if(this.projector.source === this.$definitions.PROJECTOR_SOURCE_HDMI2 && 
            this.videoMatrix.channel === this.$definitions.VIDEO_MATRIX_CHANNEL_MOBILE_TRANSMITTER) {
                return "Trasmettitore Mobile";
            }

            return "Sconosciuta";
        }
    }
}
</script>

<style>

</style>
