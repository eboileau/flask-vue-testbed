<script setup>
import { ref, onMounted } from 'vue'
import service from '@/services/index.js'

const city = ref()
const selectedCity = ref()

const product = ref()
const selectedProduct = ref()

const productTable = ref()

const productLines = ref()
const selectedLines = ref()

onMounted(() => {
  service
    .getEndpoint('/select/cities')
    .then(function (response) {
      city.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
})

const postSelectedCity = () => {
  const data = JSON.parse(JSON.stringify(selectedCity.value))
  service
    .postEndpoint('/select/cities', data)
    .then(function (response) {
      product.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
}

const postSelectedProduct = () => {
  const data = JSON.parse(JSON.stringify(selectedProduct.value))
  service
    .postEndpoint('/select/products', data)
    .then(function (response) {
      productLines.value = response.data
    })
    .catch((error) => {
      console.log(error)
    })
}

const postSelectedLines = () => {
  const data = JSON.parse(JSON.stringify(selectedLines.value))
  service
    .postEndpoint('/select/lines', data)
    .then(function (response) {
      productTable.value = response.data
    })
      .catch((error) => {
        console.log(error)
    })
}

</script>

<template>
  <div class="flex flex-col m-12">
    <h1>Dynamic dependent TreeSelect components (via API)</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
      <div>
        <TreeSelect
          @change="postSelectedCity()"
          v-model="selectedCity"
          :options="city"
          selectionMode="multiple"
          :metaKeySelection="false"
          placeholder="1. Select City"
          class="w-full md:w-20rem"
        />
      </div>
      <div>
        <TreeSelect
          @change="postSelectedProduct()"
          v-model="selectedProduct"
          :options="product"
          selectionMode="multiple"
          :metaKeySelection="false"
          placeholder="1. Select Customer (Product)"
          class="w-full md:w-20rem"
        />
      </div>
      <div>
        <MultiSelect
          @change="postSelectedLines()"
          v-model="selectedLines"
          :options="productLines"
          placeholder="Select a Line"
        />
      </div>
    </div>
    <div class="flex w-full m-6 place-content-left">
        <DataTable :value="productTable" tableStyle="min-width: 100rem">
          <Column field="customerNumber" header="Code"></Column>
          <Column field="customerName" header="Name"></Column>
          <Column field="orderNumber" header="Order"></Column>
          <Column field="productName" header="Product"></Column>
          <Column field="productLine" header="Line"></Column>
        </DataTable>
    </div>
  </div>
</template>
