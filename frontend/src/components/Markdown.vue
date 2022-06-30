<template>
  <div class="prose max-w-none" v-html="marked.parse(markdown)"></div>
</template>

<script setup>
import {marked} from 'marked'

const {markdown} = defineProps(['markdown'])
</script>
