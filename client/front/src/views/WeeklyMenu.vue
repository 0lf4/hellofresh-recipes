<script lang="ts">
  import Filter from "@/components/Filter.vue";
  import axios from "axios";
  import Menu from "@/components/Menu.vue";

  export default {
  components: {
    Menu,
    Filter
  },
};

</script>

<template>
  <Filter/>
  <Menu/>
</template>

<style scoped>

</style>
