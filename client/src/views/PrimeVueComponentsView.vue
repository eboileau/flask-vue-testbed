<script setup>
import NavigationBar from '@/components/layout/NavigationBar.vue'
import SimpleDropdown from '@/components/components/SimpleDropdown.vue'
import DependentSelect from '@/components/components/DependentSelect.vue'
import DependentSelect2 from '@/components/components/DependentSelect2.vue'
</script>

<template>
  <div class="m-6">
    <NavigationBar />
  </div>
  <Divider />
  <div class="flex flex-col">
    <div>
      <SimpleDropdown />
    </div>
    <div>
      <!-- <DependentSelect /> -->
    </div>
    <div>
      <DependentSelect2 />
    </div>
  </div>
</template>
