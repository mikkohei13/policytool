<template>
  <footer class="w-full p-6 flex bg-grey-light bottom-0 fixed text-blue-dark">
    <div class="flex flex-col justify-center">
      <a href="https://dissco.eu" target="_blank" class="block py-1">DiSSCo
        <VueFeather type="external-link" size="1rem"/>
      </a>
      <a href="https://github.com/DiSSCo/policytool" target="_blank" class="block">Source code
        <VueFeather type="external-link" size="1rem"/>
      </a>
    </div>
    <div class="grow"></div>
    <div class="flex flex-row justify-center">
      <a href="https://joint-research-centre.ec.europa.eu" target="_blank" class="place-self-center">
        <img src="/eu-logo.png" alt="european union" class="object-contain h-16">
      </a>
      <a href="https://www.eosc-portal.eu" target="_blank" title="EOSC" class="place-self-center">
        <img src="/eosc_logo.png" alt="eosc logo" class="object-contain h-20">
      </a>
    </div>
  </footer>
</template>

<script setup>
import VueFeather from 'vue-feather'
</script>
