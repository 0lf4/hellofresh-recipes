import { defineStore } from 'pinia'
import {reactive} from "vue";

export const useAppStore = defineStore('app', {
  state: () => reactive({
    recipes: [],
    filters: [],
  }),


  actions: {
    setRecipes(newRecipes: any) {
      this.recipes = newRecipes;
    },
    addFilter(filter: any) {
      this.filters.push(filter as never);
    },
    removeFilter(filter: any) {
      this.filters = this.filters.filter(f => f !== filter);
    },
    removeAllFilters() {
      this.filters = [];
    }
  }
})
