<script setup>
import { ref, onMounted } from 'vue'
import service from '@/services/index.js'

const selectedCity = ref('')
const cities = ref()
const customers = ref()

const endpoints = ['/dropdown/cities', '/dropdown/customers']

onMounted(() => {
  service
    .getConcurrent(endpoints)
    .then(function (response) {
      cities.value = response[0].data
      // selectedCity.value = cities.value[0]
      customers.value = response[1].data
    })
    .catch((error) => {
      console.log(error)
    })
})
</script>

<template>
  <div class="flex flex-col m-12">
    <h1>A simple PrimeVue Dropdown</h1>
    <div class="flex mt-6 w-full">
      <Dropdown
        v-model="selectedCity"
        :options="cities"
        optionLabel="city"
        placeholder="Select a City"
      />
    </div>
    <!-- careful... https://vuejs.org/guide/essentials/list.html#v-for-with-v-if-->
    <div class="mt-6">
    <template v-for="customer in customers" :key="customer.customerNumber">
      <li v-if="customer.city==selectedCity.city">
        {{ customer.customerName }},
        {{ customer.city }},
        {{ customer.country }}
      </li>
    </template>
    </div>
  </div>
</template>
