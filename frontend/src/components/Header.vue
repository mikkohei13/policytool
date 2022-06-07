<template>
  <header class="w-full p-6 h-28 flex bg-transparent border-b-2 border-white/25">
    <router-link :to="{name: 'home'}" class="flex-none">
      <img src="/dissco-logo-web.svg" alt="DiSSCo logo" class="h-full">
    </router-link>
    <div class="grow" />
    <Menu :items="items" class="flex-none"/>
  </header>
</template>

<script setup>
import {reactive} from "vue";
import Menu from "@/components/Menu.vue";

const items = reactive([
  {title: 'Dashboards', to: {name: 'dashboards'}, visible: true},
  {title: 'Policies', to: {name: 'policies'}, visible: true},
  {title: 'Institutions', to: {name: 'institutions'}, visible: true},
  {title: 'Log in', to: {name: 'login'}, visible: true}
])
</script>
