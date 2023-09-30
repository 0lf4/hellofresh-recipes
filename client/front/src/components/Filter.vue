<script lang="ts">
import axios from "axios";
import {useAppStore} from "@/store/app";

const API_URL = import.meta.env.VITE_API_URL;

export default {
  setup() {
    const store = useAppStore()
    const updateRecipes = (newRecipes: Array<any>) => {
      store.setRecipes(newRecipes);
    }


    const addNewFilter = (filter: Array<string>) => {
      store.removeAllFilters()
      store.addFilter(filter);
    }


    return {
      updateRecipes,
      addNewFilter,
      store
    }


  },
  data: () => ({
    selectedItems: [],
    recipes: {},
    items: ['Fruits à coque', 'Amandes', 'Lait', 'Moutarde', 'Œuf', 'Soja', 'Gluten', 'Blé', 'Arachides',
      'Graines de sésame', 'Anhydride sulfureux et sulfites', 'Poisson', 'Seigle', 'Céleri', 'Noix de pécan', 'Noisettes',
      'Noix', 'Noix de cajou', 'Porc', 'Végétarien', 'Crustacés', 'Rapido', 'Famille', 'Épicé', 'Orge', 'Avoine'],
  }),
  created: function () {
    this.items.sort((a, b) => a.localeCompare(b));
  },
  watch: {
    selectedItems(val) {
      this.selectedItems = val;
    }
  },
  methods: {
    onClick() {

      const baseUrl = API_URL + '/weekly-recipe'
      let queryString = '';

      if (this.selectedItems.length > 0) {
        queryString = this.selectedItems.map(filter => `filter=${filter}`).join('&');
      }

      const fullUrl = `${baseUrl}?${queryString}`;


      axios.get(fullUrl).then(async response => {
        let results = JSON.parse(await response.request.response).data
        this.recipes = results
        this.updateRecipes(results)
        this.addNewFilter(this.selectedItems)
      }).catch(error => {
        console.log(error)
      })
    },
  }
}
</script>

<template>
  <v-row class="mx-5 mt-5 reduced-height-row">
    <v-autocomplete
        v-model="selectedItems"
        :items=items
        chips
        clearable
        label="Choose filters"
        multiple
        variant="underlined"
    ></v-autocomplete>
  </v-row>
  <v-btn @click="onClick">Get Weekly Menu !</v-btn>
  <v-row>

  </v-row>
</template>

<style scoped>
.reduced-height-row {
  height: 50%;
}
</style>
