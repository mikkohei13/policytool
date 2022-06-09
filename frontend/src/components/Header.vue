<template>
  <header class="w-full p-6 h-28 flex bg-transparent border-b-2 border-white/25">
    <router-link :to="{name: 'home'}" class="flex-none">
      <img src="/dissco-logo-web.svg" alt="DiSSCo logo" class="h-full">
    </router-link>
    <div class="grow"/>
    <Menu :items="items" class="flex-none"/>
  </header>
</template>

<script setup>
import {reactive, watch} from "vue"
import Menu from "@/components/Menu.vue"
import {useAuth} from '@/store/auth'
import {storeToRefs} from 'pinia'

const authStore = useAuth()
const {user} = storeToRefs(authStore)

const loginItem = {title: 'Log in', to: {name: 'login'}, visible: true}
const logoutItem = {title: 'Log out', to: {name: 'logout'}, visible: true}

const items = reactive([
  {title: 'Dashboards', to: {name: 'dashboards'}, visible: true},
  {title: 'Policies', to: {name: 'policies'}, visible: true},
  // the login/logout item is always last
  loginItem
])

const updateLoginLogoutItem = (newUser) => {
  items[items.length - 1] = !newUser ? loginItem : logoutItem
}
updateLoginLogoutItem(user.value)
watch(user, updateLoginLogoutItem)

</script>
