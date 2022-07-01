<template>
  <form class="flex flex-col py-4 gap-y-0.5 items-center">
    <input v-model="username" ref="usernameInput" type="text" placeholder="username" class="w-72">
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
import {onMounted, ref} from 'vue'
import {useAuth} from '@/store/auth'
import {storeToRefs} from 'pinia'
import {useRouter, useRoute} from 'vue-router'
import {notify} from '@kyvg/vue3-notification'

const username = ref(null)
const password = ref(null)
const usernameInput = ref(null)

const router = useRouter()
const route = useRoute()
const authStore = useAuth()
const {user} = storeToRefs(authStore)
const {login, logout} = authStore

onMounted(() => usernameInput.value.focus())

const logoutPath = router.resolve({name: 'logout'}).href
const submit = async () => {
  const notification = {}

  if (await login(username.value, password.value)) {
    let onwards = route.query.to || router.options.history.state.back
    // if neither the query string nor the previous page have a valid value, just go home
    if (!onwards || onwards === logoutPath) {
      onwards = {name: 'home'}
    }
    notification.title = 'Logged in'
    notification.type = 'success'
    await router.push(onwards)
  } else {
    notification.title = 'Login failed, please try again'
    notification.type = 'error'
  }
  notify(notification);
  username.value = null
  password.value = null
}
</script>
