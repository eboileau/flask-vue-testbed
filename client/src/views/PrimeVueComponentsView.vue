<script setup>
import NavigationBar from '@/components/layout/NavigationBar.vue'
import SimpleDropdown from '@/components/components/SimpleDropdown.vue'
import DependentSelect from '@/components/components/DependentSelect.vue'
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
      <DependentSelect />
    </div>
  </div>
</template>
