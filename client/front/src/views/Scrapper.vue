<script lang="ts">

import axios from "axios";

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

      axios.get('http://localhost:8000/web_service/?lang='+ this.selectedLang).then(async response => {
                this.results = JSON.parse(await response.request.response).data
                    this.recipes = this.results
                    this.emitData()
              }).catch(error => {
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
