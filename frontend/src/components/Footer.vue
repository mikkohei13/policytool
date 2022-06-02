<template>
  <footer class="w-full p-6 flex-col bg-grey-light bottom-0 fixed text-blue-dark">
    <div class="flex flex-col">
      <a href="https://dissco.eu" target="_blank">DiSSCo
        <VueFeather type="external-link" size="1rem"/>
      </a>
      <a href="https://github.com/DiSSCo/policytool" target="_blank">Source code
        <VueFeather type="external-link" size="1rem"/>
      </a>
    </div>
    <div class="grow text-center flex-col">
      <div class="mx-auto flex justify-center">
        <a href="https://joint-research-centre.ec.europa.eu" target="_blank">
          <img src="/eu-logo.png" alt="european union" class="object-contain h-10">
        </a>
        <a href="https://www.eosc-portal.eu" target="_blank" title="EOSC ">
          <img src="/eosc_logo.png" alt="eosc logo" class="object-contain h-10">
        </a>
      </div>
      <p>H2020-INFRADEV-2019-2020 – Grant Agreement No. 871043.</p>
      <p>Funded by the Horizon 2020 Framework Programme of the European Union</p>
    </div>
  </footer>
</template>

<script setup>
import VueFeather from 'vue-feather'
</script>
