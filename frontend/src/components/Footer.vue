<template>
  <footer class="w-full p-6 flex text-blue-dark bg-white/70 border-t-2 border-white/25">
    <div class="flex flex-col justify-center">
      <a href="https://dissco.eu" target="_blank" class="block py-1">
        DiSSCo
        <VueFeather type="external-link" size="1rem"/>
      </a>
      <a href="https://github.com/DiSSCo/policytool" target="_blank" class="block py-1">
        Source code
        <VueFeather type="external-link" size="1rem"/>
      </a>
      <a href="https://unsplash.com/photos/HYTwWSE5ztw" target="_blank" class="block py-1">
        Background photo by Zdeněk Macháček on Unsplash
        <VueFeather type="external-link" size="1rem"/>
      </a>
    </div>
    <div class="grow"></div>
    <div class="flex flex-col items-end md:flex-row md:justify-center md:items-center">
      <a href="https://joint-research-centre.ec.europa.eu" target="_blank">
        <img src="/eu-logo.png" alt="european union" class="object-contain h-16">
      </a>
      <a href="https://www.eosc-portal.eu" target="_blank" title="EOSC">
        <img src="/eosc_logo.png" alt="eosc logo" class="object-contain h-20">
      </a>
    </div>
  </footer>
</template>

<script setup>
import VueFeather from 'vue-feather'
</script>
