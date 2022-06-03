<template>
  <div @mouseover="show" @mouseleave="hide" class="flex flex-col">
    <div class="flex flex-row-reverse">
      <button class="p-2 pb-1 rounded text-white hover:text-grey">
        <VueFeather type="menu" size="2rem"></VueFeather>
      </button>
    </div>
    <ul v-if="visible" class="bg-white p-0 border-solid border-t-2 border-yellow cursor-pointer z-10">
      <li v-for="item in visibleItems">
        <router-link :to="item.to" @click="hide" class="text-lg hover:bg-grey py-1 px-5 block w-full">
          {{ item.title }}
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import {computed, ref} from 'vue'
import VueFeather from 'vue-feather'

const {items} = defineProps(['items'])
let visible = ref(false);

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
