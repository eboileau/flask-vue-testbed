<script setup>
import NavigationBar from '@/components/layout/NavigationBar.vue'

defineProps({
  header: {
    type: String,
    required: true
  },
  msg: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="m-6">
    <NavigationBar />
  </div>
  <Divider />
  <div class="grid grid-cols-2 p-6">
    <div class="text-left flex align-baseline">
      <section>
        <span class="block text-6xl font-bold mb-1">{{ header }}</span>
        <div class="text-6xl font-bold mb-3 text-blue-600">{{ msg }}</div>
        <p class="mt-0 mb-4 leading-loose">MySQL + Flask + VueJS SPA (with Tailwind CSS, PrimeVue)</p>
      </section>
    </div>
    <div>
      <img src="@/assets/images/p0fg687j.webp" alt="Image" class="md:ml-auto block md:h-full" style="clip-path: polygon(8% 0, 100% 0%, 100% 100%, 0 100%)">
    </div>
  </div>
</template>

<style scoped>
</style>
