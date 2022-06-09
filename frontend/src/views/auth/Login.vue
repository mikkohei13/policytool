<template>
  <form class="flex flex-col py-4 gap-y-0.5 items-center">
    <input v-model="username" type="text" placeholder="username" class="w-72">
    <input v-model="password" type="password" placeholder="password" class="w-72">
    <button @click.prevent="submit" class="bg-yellow my-4 p-3 rounded hover:bg-yellow-dark w-72">
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
import {useRouter} from 'vue-router'

const username = ref(null);
const password = ref(null);
const authStore = useAuth()
const {user} = storeToRefs(authStore)
const {login, logout} = authStore
const router = useRouter()

const submit = async () => {
  await login(username.value, password.value)
  // redirect back to the previous page (or the homepage if there is no previous page)
  const previous = router.options.history.state.back || '/'
  await router.push(previous)
}
</script>
