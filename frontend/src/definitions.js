import Vue from 'vue'

const definitions = {
    PROJECTOR_SOURCE_HDMI1: 2,
    PROJECTOR_SOURCE_HDMI2: 3,
    PROJECTOR_SOURCE_VGA: 0,
    VIDEO_MATRIX_CHANNEL_APPLE_TV: 1,
    VIDEO_MATRIX_CHANNEL_MOBILE_TRANSMITTER: 2,
};

export default {
    install() {
        Object.defineProperty(Vue.prototype, '$definitions', {
            get () { return definitions }
        });
    }
};