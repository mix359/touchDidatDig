<template>
    <div>
        <div class="card text-center z-depth-2 ripple-parent button-box" :class="buttonColor" @click="clicked">
            <div class="card-body" v-if="icon">
                <h1 class="white-text mb-0"><i class="fa" :class="icon"></i></h1>
            </div>
            <div class="card-footer text-muted white-text">
                <p class="mb-0">{{text}}</p>
            </div>
        </div>
    </div>
</template>

<script>
import { waves } from 'mdbvue';

export default {
    mixins: [waves],
    props: {
        text: {default: ""},
        icon: {default: ""},
        color: {default: "mdb-color"},
        activeColor: {default: "mdb-color lighten-2"},
        isActive: {default: false}
    },
    data: () => ({
        waves: true
    }),
    computed: {
        buttonColor() {
            return this.isActive ? this.activeColor : this.color;
        }
    },
    methods: {
        clicked(e) {
            this.wave(e);
            this.$emit("click", e);
        }
    }
}
</script>

<style lang="scss" scoped>
    .button-box {
        cursor: pointer;
        transition: box-shadow 0.3s;
        &:hover {
            -webkit-box-shadow: 0 5px 11px 0 rgba(0,0,0,.18),0 4px 15px 0 rgba(0,0,0,.15);
            box-shadow: 0 5px 11px 0 rgba(0,0,0,.18),0 4px 15px 0 rgba(0,0,0,.15);
        }
    }
</style>
