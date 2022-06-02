<template>
  <header class="w-full p-6 h-28 flex bg-blue">
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
  {title: 'Dashboards', link: '/dashboards', visible: true},
  {title: 'Policies', link: '/policies', visible: true},
  {title: 'Institutions', link: '/institutions', visible: true},
  {title: 'Log in', link: '/login', visible: true}
])
</script>
