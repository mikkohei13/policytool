<template>
  <p class="text-white">
    {{ pack.name }}
  </p>
</template>

<script setup>
// TODO: this is currently written to only work with policy packs
// TODO: if you get to this view without loading the institution home view first it breaks
import {useStore} from '@/store/main'
import {useRouter} from 'vue-router'

const router = useRouter()
const {id} = defineProps(['id'])
const {getPack} = useStore()
const pack = getPack(id)

</script>
