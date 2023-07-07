<script setup>
import { ref, onMounted } from 'vue'
import service from '@/services/index.js'

const city = ref()
const selectedCity = ref()

const product = ref()
const selectedProduct = ref()

const productTableFull = ref()
const productTableWkg = ref()
const productTable1 = ref()
const productTable2 = ref()
const productTable = ref()

const productLines = ref()
const selectedLines = ref()

const dt = ref()
const loading = ref(false)
const totalRecords = ref(0)
const lazyParams = ref({})

onMounted(() => {
  loading.value = true

  lazyParams.value = {
    first: 0,
    rows: dt.value.rows,
    // sortField: null,
    // sortOrder: null,
    // filters: filters.value
  }


  service
    .getEndpoint('/select/cities')
    .then(function (response) {
      city.value = response.data.tree
      productTableFull.value = response.data.records
      productTableWkg.value = productTableFull.value
      totalRecords.value = response.data.totalRecords
      loadLazyData()
    })
    .catch((error) => {
      console.log(error)
    })


})

// const loadLazyData = () => {
//   loading.value = true
//   console.log('LAZY', lazyParams.value)
//   setTimeout(() => {
//     service
//       .getEndpoint('https://www.primefaces.org/data/customers')
//       .then((data) => {
//         productTable.value = data.data.customers.slice(
//           lazyParams.value.first,
//           lazyParams.value.first + lazyParams.value.rows
//         )
//       totalRecords.value = data.data.totalRecords
//       loading.value = false
//     })
//   }, Math.random() * 1000 + 250)
// }


// we're not actually lazy loading? should we make an API call each time
// to update the table?

const loadLazyData = () => {
  loading.value = true
  productTable.value = productTableWkg.value.slice(
    lazyParams.value.first,
    lazyParams.value.first + lazyParams.value.rows
  )
  loading.value = false
  // service
  //   .getEndpoint('/select/cities')
  //   .then(function (response) {
  //     productTable.value = response.data.records.slice(
  //       lazyParams.value.first,
  //       lazyParams.value.first + lazyParams.value.rows
  //     )
  //     totalRecords.value = response.data.totalRecords
  //     loading.value = false
  //   })
  //   .catch((error) => {
  //     console.log(error)
  //   })
}

const onPage = (event) => {
  lazyParams.value = event
  loadLazyData()
}

// const onSort = (event) => {
//   lazyParams.value = event;
//   loadLazyData()
// }

// const onFilter = () => {
//   lazyParams.value.filters = filters.value ;
//   loadLazyData()
// }

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
  // no need to use hasOwnProperty because deserializing the JSON in data
  // const dataArray = []
  var dataArray = Object.keys(data)
  //  console.log('ARRAY', dataArray)
  // console.log('TYPE', Array.isArray(dataArray))
  //data.forEach(k => dataArray.push(k))
  // console.log('CHECK', dataArray.includes('Graz'))
  // const key
  // for (key in data) {
  //   dataArray.push(key)
  // }
  // console.log('VALUE', data)
  //console.log('TYPE', Array.isArray(data))
  // update table
  productTableWkg.value = productTableFull.value.filter(value =>
    dataArray.includes(value.country) ||
    dataArray.includes(value.city)
  )
  totalRecords.value = productTableWkg.value.length
  productTable1.value = productTableWkg.value
  selectedProduct.value = null
  selectedLines.value = null
  loadLazyData()
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
  // do we need this series of tmp tables?
  // filtering by city/country maybe redundant for customer/order, but not product
  // but what about our main application?
  var dataArray = Object.keys(data)
  productTableWkg.value = productTable1.value.filter(value =>
    dataArray.includes(value.customerName) ||
    dataArray.includes(value.orderNumber.toString()) ||
    dataArray.includes(value.productName)
  )
  productTable2.value = productTableWkg.value
  totalRecords.value = productTableWkg.value.length
  selectedLines.value = null
  loadLazyData()
}

const postSelectedLines = () => {
  const data = JSON.parse(JSON.stringify(selectedLines.value))
  // this is an array here
  productTableWkg.value = productTable2.value.filter(value => data.includes(value.productLine)) 
  totalRecords.value = productTableWkg.value.length
  loadLazyData()
}
// const postSelectedLines = () => {
//   const data = JSON.parse(JSON.stringify(selectedLines.value))
//   service
//     .postEndpoint('/select/lines', data)
//     .then(function (response) {
//       productTable.value = response.data
//     })
//       .catch((error) => {
//         console.log(error)
//     })
// }

</script>

<template>
  <div class="flex flex-col m-12">
    <h1>Dynamic dependent TreeSelect components (via API) VERSION 2</h1>
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
      <DataTable
        :value="productTable"
        lazy paginator
        :rows="10"
        ref="dt"
        :totalRecords="totalRecords"
        :loading="loading"
        @page="onPage($event)"
        tableStyle="min-width: 100rem">
        <!-- <Column field="name" header="Name"></Column>
             <Column field="country.name" header="Country"></Column>
             <Column field="company" header="Cie"></Column> -->
        <Column field="customerNumber" header="Code"></Column>
        <Column field="customerName" header="Name"></Column>
        <Column field="orderNumber" header="Order"></Column>
        <Column field="productName" header="Product"></Column>
        <Column field="productLine" header="Line"></Column>
      </DataTable>
    </div>
  </div>
</template>
