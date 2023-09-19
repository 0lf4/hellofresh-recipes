<script lang="ts">
import axios from "axios";

export default {
  data: () => ({
    loading: false,
    selection: 1,
    results: []
  }),

  methods: {
    reserve() {
      this.loading = true

      setTimeout(() => (this.loading = false), 2000)
    },
  },

  mounted() {
    axios.get('http://localhost:8000/').then(async response => {
      this.results = JSON.parse(await response.request.response).data
    }).catch(error => {
      console.log(error)
    })
  }
}
</script>

<template>

  <v-row class="mx-5 mt-5">
    <v-autocomplete
      clearable
      chips
      label="Choose filters"
      :items="['California', 'Colorado', 'Florida', 'Georgia', 'Texas', 'Wyoming']"
      multiple
      variant="underlined"
    ></v-autocomplete>
  </v-row>

  <v-row class="mx-5 mt-5">
    <v-col
      v-for="recipe in results"
      :key="recipe"
      cols="6"
      sm="3"
      md="4"
    >

      <v-card :title="recipe.name" class="custom-card">

        <v-card-item>
          <v-card-title>{{ recipe._source.name }}</v-card-title>
          <v-card-subtitle>{{ recipe._source.difficulty }} • {{ recipe._source.time }}</v-card-subtitle>

          <div v-if="recipe._source.allergen.length > 0 && recipe._source.tags.length > 0">
            <h4>Tags</h4>
            <v-chip-group v-model="selection" class="d-flex flex-wrap">
              <v-chip v-for="element in recipe._source.allergen.concat(recipe._source.tags)" :key="element">{{
                  element
                }}
              </v-chip>
            </v-chip-group>
          </div>

          <v-card-actions>
            <v-btn
              color="orange-lighten-2"
              variant="text"
            >
              Details
            </v-btn>

            <v-spacer></v-spacer>

            <v-btn
              :icon="recipe.showDetails ? 'mdi-chevron-up' : 'mdi-chevron-down'"
              @click="recipe.showDetails = !recipe.showDetails"
            ></v-btn>
          </v-card-actions>

          <v-expand-transition>
            <div v-show="recipe.showDetails">
              <v-divider></v-divider>

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

            </div>
          </v-expand-transition>
        </v-card-item>
      </v-card>


    </v-col>
  </v-row>
</template>

<style scoped>

</style>
