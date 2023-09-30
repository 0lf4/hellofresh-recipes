<script lang="ts">

import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;


export default
{
  name: 'Scrapper',
  data() {
    return {
      selectedLang: '',
    }
  },
  watch: {
    selectedLang(val) {
      this.selectedLang = val;
    }
  },
  methods: {
    startScrap() {

      axios.get(API_URL + '/web_service/?lang='+ this.selectedLang).catch(error => {
                console.log(error)
              })
    }
  }
};
</script>

<template>

    <div class="mx-5 mt-5">
    <v-combobox
    label="Choose a sitemap"
    v-model="selectedLang"
    :items="[
            'UK',
            'COM',
            'FR',
            'DE',
            'ES',
            'NL',
            'BE',
            'LU',
            'CH',
            'IT']"
    ></v-combobox>

    <v-btn @click="startScrap()"> Start Scrapping</v-btn>

    </div>
</template>

<style scoped>

</style>
