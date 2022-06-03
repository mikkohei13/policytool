<template>
  <div class="p-4 mx-auto max-w-screen-2xl">
    <p class="text-3xl text-blue-dark font-bold">DiSSCo Policy and Digital Readiness Assessment Tool</p>
    <!-- TODO: need some copy here! -->
    <p>Some text about the Policy Tool.</p>
    <br/>
    <br/>
    <br/>
    <div class="flex flex-row gap-4">
      <router-link :to="{name: 'policies'}" class="bg-yellow p-3 rounded hover:bg-yellow-dark">
        Explore policies
        <VueFeather type="chevron-right" size="2rem" class="align-middle "></VueFeather>
      </router-link>
      <router-link :to="{name: 'login'}" class="bg-yellow p-3 rounded hover:bg-yellow-dark">
        Login/Register
        <VueFeather type="chevron-right" size="2rem" class="align-middle "></VueFeather>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import VueFeather from 'vue-feather'
</script>
