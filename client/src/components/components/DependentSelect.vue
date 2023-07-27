<script setup>
import { ref, onMounted } from 'vue'
import service from '@/services/index.js'

const city = ref()
const selectedCity = ref()

const product = ref()
const selectedProduct = ref()

const selectOptions = ref()
const productTable = ref()

const productLines = ref()
const selectedLines = ref()

const dt = ref()
const loading = ref(false)
const totalRecords = ref(0)
const lazyParams = ref({})

function toTree(data, keys) {
  var tree = data.reduce((r, o) => {
    keys.reduce((t, k) => {
      var tmp = (t.children = t.children || []).find(p => p.key === o[k])
      if (!tmp) {
        t.children.push(tmp = { "key": o[k], "label": o[k] })
      }
      return tmp
    }, r)
    return r
  }, {}).children
  return tree
}

onMounted(() => {
  lazyParams.value = {
    first: 0,
    rows: dt.value.rows,
    // sortField: null,
    // sortOrder: null,
    // filters: filters.value
  }
  lazyLoad()
  service
    .getEndpoint('/select')
    .then(function (response) {
      selectOptions.value = response.data.records
      city.value = toTree(selectOptions.value, ["country", "city"])
    })
    .catch((error) => {
      console.log(error)
    })
})

function lazyLoad() {
  loading.value = true
  service
    .get('/search', {
      params: {
        'city': toParams(selectedCity.value),
        'product': toParams(selectedProduct.value),
        'line': selectedLines.value,
        'firstRecord': lazyParams.value.first,
        'maxRecords': lazyParams.value.rows
      },
      paramsSerializer: {
        indexes: null
      }
    })
    .then(function (response) {
      productTable.value = response.data.records
      totalRecords.value = response.data.totalRecords
    })
    .catch((error) => {
      console.log(error)
    })
  loading.value = false
}

const onPage = (event) => {
  lazyParams.value = event
  lazyLoad()
}

// const onSort = (event) => {
//   lazyParams.value = event;
//   lazyLoad()
// }

// const onFilter = () => {
//   lazyParams.value.filters = filters.value ;
//   lazyLoad()
// }

function toParams(model) {
  // this is not great, we need a better way to handle this...
  if (!(model === undefined)) {
    return Object.keys(JSON.parse(JSON.stringify(model)))
  }
  return []
}

const postSelectedCity = () => {
  selectedProduct.value = undefined
  selectedLines.value = undefined
  var selected = Object.keys(JSON.parse(JSON.stringify(selectedCity.value)))
  var options = selectOptions.value.filter(item => selected.includes(item.country) || selected.includes(item.city))
  product.value = toTree(options, ["customerName", "orderNumber", "productName"])
  lazyLoad()
}

const postSelectedProduct = () => {
  selectedLines.value = undefined
  var selected = Object.keys(JSON.parse(JSON.stringify(selectedProduct.value)))
  // integer vs. string...
  var options = selectOptions.value.filter(item => selected.includes(item.productName) || selected.includes(String(item.orderNumber)) || selected.includes(item.customerName))
  productLines.value = [...new Set(options.map(item => item.productLine))]
  lazyLoad()
}

const postSelectedLines = () => {
  lazyLoad()
}

</script>

<template>
  <div class="flex flex-col m-12">
    <h1>Dynamic dependent TreeSelect components (via API) VERSION 4</h1>
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
