<template>
  <article class="bg-home-image flex flex-col items-stretch min-h-screen bg-top bg-cover">
    <Header class="shrink-0"/>
    <main class="grow shrink-0">
      <div class="p-4 py-8 mx-auto max-w-screen-xl">
        <router-view/>
      </div>
    </main>
    <Footer class="shrink-0"/>
  </article>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
</script>
