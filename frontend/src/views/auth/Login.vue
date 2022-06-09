<template>
  <form class="flex flex-col py-4 gap-y-0.5 items-center">
    <input v-model="username" type="text" placeholder="username" class="w-72">
    <input v-model="password" type="password" placeholder="password" class="w-72">
    <button @click="submit" class="bg-yellow my-4 p-3 rounded hover:bg-yellow-dark w-72">
      Login
    </button>

    <div class="flex flex-col items-center">
      <router-link :to="{name: 'resetPassword'}" class="text-white py-2 border-b border-white">
        Click here to reset your password
      </router-link>
      <router-link :to="{name: 'requestAccount'}" class="text-white py-2">
        Request an account
      </router-link>
    </div>
  </form>
</template>

<script setup>
import {ref} from 'vue';
import {useAuth} from '@/store/auth'
import {storeToRefs} from "pinia";

const username = ref(null);
const password = ref(null);
const authStore = useAuth()
const user = storeToRefs(authStore)
const {login, logout} = authStore

const submit = async (e) => {
  e.preventDefault()
  await login(username.value, password.value)
}
</script>
