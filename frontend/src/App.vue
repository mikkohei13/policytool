<template>
    <article class="bg-home-image flex flex-col items-stretch min-h-screen bg-center bg-cover">
      <Header class="shrink-0" />
      <main class="grow shrink-0">
        <router-view/>
      </main>
      <Footer class="shrink-0" />
    </article>
</template>

<script setup>
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
</script>
