<template>
  <h1 class="text-3xl font-bold text-white">Logged out successfully</h1>
</template>

<script setup>
import {useAuth} from '@/store/auth'
import {onMounted} from 'vue'

const {logout} = useAuth()

onMounted(async () => {
  await logout()
})

</script>
