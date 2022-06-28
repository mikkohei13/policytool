<template>
  <div @mouseover="show" @mouseleave="hide" class="flex flex-col relative">
    <button class="p-2 pb-1 rounded text-white hover:text-grey place-self-end">
      <VueFeather type="menu" size="2rem"></VueFeather>
    </button>
    <Fade>
      <ul v-if="visible"
          class="absolute right-0 top-full bg-white p-0 border-solid border-t-2 border-yellow cursor-pointer z-10 w-56">
        <li v-for="item in visibleItems">
          <router-link v-if="item.to" :to="item.to" @click="hide"
                       class="text-lg hover:bg-grey first:pt-2 pb-2 px-8 block w-full">
            {{ item.title }}
          </router-link>
          <span v-if="!item.to" @click="item.func"
                class="text-lg hover:bg-grey first:pt-2 pb-2 px-8 block w-full">
            {{ item.title }}
          </span>
        </li>
      </ul>
    </Fade>
  </div>
</template>

<script setup>
import {computed, ref} from 'vue'
import Fade from '@/components/transitions/Fade.vue'

const {items} = defineProps(['items'])
let visible = ref(false)

/**
 * Returns a list of menu items that should be shown when the menu is displayed.
 */
const visibleItems = computed(() => {
  return items.filter(item => item.visible)
})

/**
 * Shows the menu.
 */
const show = () => {
  visible.value = true
}

/**
 * Hides the menu.
 */
const hide = () => {
  visible.value = false
}
</script>
