// Utilities
import { defineStore } from 'pinia'
import {reactive} from "vue";

export const useAppStore = defineStore('app', {
  state: () => reactive({
    recipes: [],
    filters: [],
  }),


  actions: {
    setRecipes(newRecipes) {
      this.recipes = newRecipes;
    },
    addFilter(filter) {
      this.filters.push(filter);
    },
    removeFilter(filter) {
      this.filters = this.filters.filter(f => f !== filter);
    },
    removeAllFilters() {
      this.filters = [];
    }
  }
})
