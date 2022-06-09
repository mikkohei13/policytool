<template>
  <header class="w-full p-6 h-28 flex bg-transparent border-b-2 border-white/25 items-center">
    <router-link :to="{name: 'home'}" class="flex-none">
      <img src="/dissco-logo-web.svg" alt="DiSSCo logo" class="h-16">
    </router-link>
    <div class="grow"/>
    <div v-if="loggedIn" class="text-white pr-2 border-r">
      {{ displayName }}
    </div>
    <Menu :items="items"/>
  </header>
</template>

<script setup>
import {computed, reactive} from "vue"
import Menu from "@/components/Menu.vue"
import {useAuth} from '@/store/auth'
import {storeToRefs} from 'pinia'

const {user, loggedIn, notLoggedIn} = storeToRefs(useAuth())

const displayName = computed(() => `${user.value.first_name} ${user.value.last_name}`)

const items = reactive([
  {title: 'Dashboards', to: {name: 'dashboards'}, visible: true},
  {title: 'Policies', to: {name: 'policies'}, visible: true},
  {title: 'Log in', to: {name: 'login'}, visible: notLoggedIn},
  {title: 'Log out', to: {name: 'logout'}, visible: loggedIn}
])

</script>
