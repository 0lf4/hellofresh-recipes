<script lang="ts">


import axios from "axios";
import {useAppStore} from "@/store/app";
import {reactive, watch} from "vue";

const API_URL = import.meta.env.VITE_API_URL;

type StateType = {
    Recipes: any[];
    localFilters: any[];
};

export default {
  setup() {
    const store = useAppStore();

    const state = reactive<StateType>({
      Recipes: [...store.recipes],
      localFilters: [...store.filters]
    });

    watch(() => store.recipes, (newVal) => {
      state.Recipes = newVal;
    });

    watch(() => store.filters, (newVal) => {
      state.localFilters = newVal;
    });


    const updateRecipes = (newRecipes: any) => {
      store.setRecipes(newRecipes);
    }


    const addNewFilter = (filter: any) => {
      store.addFilter(filter);
    }


    return {
      state,
      updateRecipes,
      addNewFilter,

    };
  },
  data() {
    return {
      dialogs: {} as Record<string, boolean>,
      localRecipes: this.recipes,
      formData: {
        username: '',
        filters: [] as string[],
        recipes: [] as any[]
      }
    }
  },
  methods: {
    toggleDialog(id: any) {
      // this.$set(this.dialogs, id, !this.dialogs[id]);
      this.dialogs[id] = !this.dialogs[id];
    },
    togglePdfRecipe(pdfPath: string) {
      // this.$set(this.dialogs, id, !this.dialogs[id]);
      axios.get(API_URL + '/pdf/' + pdfPath).then(async response => {
        let results = JSON.parse(await response.request.response).data

        const blob = await results;
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.target = '_blank';
        link.click();
      }).catch(error => {
        console.log(error)
      })
    },
    onChangeRecipe(id: string) {


      const baseUrl = API_URL + '/change-one'
      let queryString = '';

      let ids = this.state.Recipes.map(recipe => recipe._id)

      queryString = `ids=${ids.join('&&')}`


      if (this.state.localFilters[0].length > 0) {
        queryString += this.state.localFilters[0].map((filter: string) => `filter=${filter}`).join('&');
      }


      const fullUrl = `${baseUrl}?${queryString}`;

      axios.get(fullUrl).then(async response => {
        const updatedRecipe = JSON.parse(await response.request.response).data

        this.state.Recipes = this.state.Recipes.map(recipe => {
          if (recipe._id === id) {
            return updatedRecipe[0];
          }
          return recipe;
        });

      }).catch(error => {
        console.log(error)
      })

    },
    onSave() {
      const baseUrl = API_URL + '/save/'


      this.formData.username = 'test'
      this.formData.filters = this.state.localFilters[0]
      this.formData.recipes = this.state.Recipes

      axios.post(baseUrl, this.formData).catch(error => {
        console.log(error)
      })

    },
    onClick() {

      const baseUrl = API_URL + '/menu/get-back/test'

      axios.get(baseUrl).then(async response => {
        const updatedRecipe = JSON.parse(await response.request.response).data
        this.state.Recipes = updatedRecipe[0]._source.recipes;
        this.state.localFilters = updatedRecipe[0]._source.filters;
        console.log(updatedRecipe[0]._source.filters)

      }).catch(error => {
        console.log(error)
      })
    },
  }
};
</script>

<template>
  <v-row class="mx-5 mt-5">
    <v-btn @click="onSave">Save</v-btn>
    <v-btn @click="onClick">Get saved weekly menu</v-btn>
  </v-row>


  <v-row class="mx-5 mt-5">

    <v-col
        v-for="recipe in state.Recipes"
        :key="recipe"
        cols="3"
        sm="3"
        md="3"
    >

      <v-card :title="recipe.name" class="custom-card">

        <v-btn icon class="triangle-icon" @click="onChangeRecipe(recipe._id)" flat depressed>
          <v-icon>mdi-refresh</v-icon>
        </v-btn>


        <v-card-item>
          <v-card-title>{{ recipe._source.name }}</v-card-title>
          <v-card-subtitle>{{ recipe._source.difficulty }} • {{ recipe._source.time }}</v-card-subtitle>

          <div v-if="recipe._source.allergen.length > 0 && recipe._source.tags.length > 0">
            <h4>Tags</h4>
            <v-chip-group class="d-flex flex-wrap">
              <v-chip v-for="element in recipe._source.allergen.concat(recipe._source.tags)" :key="element">{{
                  element
                }}
              </v-chip>
            </v-chip-group>
          </div>

          <v-card-actions>


            <v-btn
                :icon="'mdi-chevron-up'"
                @click="togglePdfRecipe(recipe._source.pdf_local)"
            ></v-btn>


            <v-spacer></v-spacer>


            <v-dialog width="auto" v-model="dialogs[recipe._id]">
              <template v-slot:activator="{ props }">

                <v-btn color="orange-lighten-2" variant="text" v-bind="props" @click="toggleDialog(recipe._id)">
                  Details
                </v-btn>

              </template>


              <v-card>

                <v-card-item>
                  <v-card-title>{{ recipe._source.name }}</v-card-title>
                  <v-card-subtitle>{{ recipe._source.difficulty }} • {{ recipe._source.time }}</v-card-subtitle>

                  <div v-if="recipe._source.allergen.length > 0 && recipe._source.tags.length > 0">
                    <h4>Tags</h4>
                    <v-chip-group class="d-flex flex-wrap">
                      <v-chip v-for="element in recipe._source.allergen.concat(recipe._source.tags)" :key="element">{{
                          element
                        }}
                      </v-chip>
                    </v-chip-group>
                  </div>

                  <div v-if="recipe._source.utensils.length > 0">
                    <h4>Ustensiles</h4>
                    <v-card-text>
                      {{ recipe._source.utensils.join(' • ') }}
                    </v-card-text>
                  </div>

                  <div v-if="recipe._source.ingredients.length > 0">
                    <h4>Ingrédients</h4>
                    <v-row>
                      <v-col v-for="(ingredient, index) in recipe._source.ingredients" :key="index" cols="4">
                        <v-card-text>
                          <ul>
                            <li>{{ ingredient[1] }}</li>
                            <p><b>{{ ingredient[0] }}</b></p>
                          </ul>
                        </v-card-text>
                      </v-col>
                    </v-row>
                  </div>

                  <div v-if="recipe._source.instructions.length > 0">
                    <h4>Instructions</h4>
                    <v-card-text v-for="instruction in recipe._source.instructions">
                      <b>{{ instruction[0] }}</b>_ {{ instruction[1] }}
                    </v-card-text>
                  </div>

                  <v-card-actions>
                    <v-btn color="primary" block @click="dialogs = {}">Close Dialog</v-btn>
                  </v-card-actions>
                </v-card-item>

              </v-card>

            </v-dialog>


          </v-card-actions>


        </v-card-item>
      </v-card>


    </v-col>
  </v-row>
</template>

<style scoped>

.custom-card {
  height: 100%;
  position: relative;
  overflow: hidden;
}


.triangle-icon {
  position: absolute;
  top: 0;
  right: 0;
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 0 50px 50px 0;
  border-color: transparent #4602fa transparent transparent;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 0 !important;
  padding: 0 !important;
  box-shadow: none !important;
  background: none !important;


  clip-path: polygon(100% 0, 100% 100%, 0% 0%);
}

.triangle-icon:hover {
  transform: scale(1.1);
}


.triangle-icon:hover > v-icon {
  transform: translate(-50%, -50%) scale(1.1);
}

.mdi-refresh {
  color: white;
  position: absolute;
  transform: translate(140%, 65%);
}

</style>
