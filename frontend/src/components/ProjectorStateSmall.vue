<template>
    <div class="card indigo darken-2 ripple-parent" @click="onClicked">
        <div class="card-body">
            <h5>Proiettore {{projector.name}}</h5>
            <div class="float-right">
                <i class="fa fa-volume-off" v-if="projector.muted"></i>
                <i class="fa fa-snowflake-o ml-2" v-if="projector.freezed"></i>
                <i class="fa fa-square-o ml-2" v-if="projector.blanked"></i>
            </div>
            
            <div>Sorgente: {{source}}</div>

            <div>Volume:</div>
            <div class="progress md-progress" style="height: 20px">
                <div class="progress-bar" role="progressbar" style="height: 20px" :style="'width: ' + volume + '%;'" :aria-valuenow="volume" aria-valuemin="0" aria-valuemax="100">{{volume}}%</div>
            </div>
        </div>
    </div>
</template>

<script>
import { waves } from 'mdbvue';

export default {
    name: "projector-state-small",
    mixins: [waves],
    props: {
        projectorId: {required: true, type: Number}
    },
    data: () => ({
        waves: true
    }),
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
    },
    methods: {
        onClicked(e) {
            this.wave(e);
            this.$store.commit('changePage', this.projectorId);
        }
    }
}
</script>

<style scoped>
    .card {
        cursor: pointer;
    }
</style>
