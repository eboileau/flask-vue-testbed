<script setup>
  import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="flex flex-wrap [&>*]:mr-6">
  <RouterLink
    :to="{ name: 'Home'}"
  >
    <Button label="Home" type="button" class="p-button-outlined"></Button>
  </routerlink>
  <RouterLink
    :to="{ name: 'Directives'}"
  >
    <Button label="Directives" type="button" class="p-button-outlined"></Button>
  </RouterLink>
  <RouterLink
    :to="{ name: 'Components'}"
  >
    <Button label="Components" type="button" class="p-button-outlined"></Button>
  </RouterLink>
  <RouterLink
    :to="{ name: 'PrimeVueComponents'}"
  >
    <Button label="PrimeVue" type="button" class="p-button-outlined"></Button>
  </RouterLink>
  <RouterLink
    :to="{ name: 'Router'}"
  >
    <Button label="Router" type="button" class="p-button-outlined"></Button>
  </RouterLink>
  </div>
</template>
