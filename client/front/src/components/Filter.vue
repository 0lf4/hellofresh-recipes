<script lang="ts">


import axios from "axios";
import {useAppStore} from "@/store/app";
import {ref} from "vue";

export default {
  setup() {
     const store = useAppStore()
          const updateRecipes = (newRecipes) => {
      store.setRecipes(newRecipes);
    }


    const addNewFilter = (filter) => {
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
    recipes: {}
  }),
  watch: {
    selectedItems(val) {
        this.selectedItems = val;
    }
  },
    methods: {
        onClick() {

            const baseUrl = 'http://localhost:8000/weekly-recipe'
            let queryString = '';

            if (this.selectedItems.length > 0) {
                queryString = this.selectedItems.map(filter => `filter=${filter}`).join('&');
            }

             const fullUrl = `${baseUrl}?${queryString}`;


                axios.get(fullUrl).then(async response => {
                this.results = JSON.parse(await response.request.response).data
                    this.recipes = this.results


                    this.updateRecipes(this.results)

                  this.addNewFilter(this.selectedItems)


                    // this.emitData()
              }).catch(error => {
                console.log(error)
              })
        },
        // emitData() {
        //   this.$emit('filterEvent', {"recipes": this.recipes, "filters": this.selectedItems});
        // }
    }
}
</script>

<template>
    <v-row class="mx-5 mt-5 reduced-height-row">
    <v-autocomplete
      clearable
      chips
      label="Choose filters"
      :items="['Fruits à coque', 'Amandes', 'Lait', 'Moutarde', 'Œuf', 'Soja', 'Gluten', 'Blé', 'Arachides',
      'Graines de sésame', 'Anhydride sulfureux et sulfites', 'Poisson', 'Seigle', 'Céleri', 'Noix de pécan', 'Noisettes',
      'Noix', 'Noix de cajou', 'Porc', 'Végétarien', 'Crustacés', 'Rapido', 'Famille', 'Épicé', 'Orge', 'Avoine']"
      multiple
      variant="underlined"
      v-model="selectedItems"
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
