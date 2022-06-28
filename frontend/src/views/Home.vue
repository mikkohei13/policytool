<template>
  <p class="text-5xl text-white font-bold">DiSSCo Policy and Digital Maturity Assessment Tool</p>
  <!-- TODO: need some copy here! -->
  <p class="text-white">Some text about the Policy Tool.</p>
  <br/>
  <br/>
  <br/>
  <div class="flex flex-row gap-4 justify-evenly sm:justify-start">
    <template v-if="loggedIn">
      <router-link :to="{name: 'policy'}" class="bg-yellow p-3 rounded hover:bg-yellow-dark">
        Review institutional policies
        <VueFeather type="chevron-right" size="2rem" class="align-middle "></VueFeather>
      </router-link>
      <router-link :to="{name: 'maturity'}" class="bg-yellow p-3 rounded hover:bg-yellow-dark">
        Review institutional maturity
        <VueFeather type="chevron-right" size="2rem" class="align-middle "></VueFeather>
      </router-link>
    </template>
    <template v-else>
      <router-link :to="{name: 'login'}" class="bg-yellow p-3 rounded hover:bg-yellow-dark">
        Login/Register
        <VueFeather type="chevron-right" size="2rem" class="align-middle "></VueFeather>
      </router-link>
    </template>
  </div>
</template>

<script setup>
import {useAuth} from '@/store/auth'
import {storeToRefs} from 'pinia'

const {loggedIn} = storeToRefs(useAuth())
</script>