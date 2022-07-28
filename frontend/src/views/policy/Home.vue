<template>
  <div>
    <div class="text-4xl text-white font-bold pb-6">
      {{ institution.name }}
    </div>
  </div>

  <div class="flex flex-col gap-10">
    <div class="flex flex-row gap-4 pt-4">
      <div>
        <router-link :to="{name: 'policy_docs'}"
                     class="bg-yellow p-3 pl-5 rounded hover:bg-yellow-dark">
          View your institution's policy documents
          <VueFeather type="file-text" size="1.4rem" class="align-middle -mt-1"/>
        </router-link>
      </div>
      <div>
        <router-link :to="{name: 'policy_all'}"
                     class="bg-blue p-3 rounded hover:bg-blue-dark">
          View all your institution's policy responses
          <VueFeather type="activity" size="1.4rem" class="align-middle -mt-1"/>
        </router-link>
      </div>
    </div>

    <div class="bg-white rounded p-4">
      <div class="text-xl border-b-2 border-yellow pb-2">
        DiSSCo Service Policy Alignment
      </div>
      <div class="flex flex-col gap-2">
        <div v-for="service in services"
             class="flex flex-row gap-2 items-center p-2 hover:bg-grey-light">
          <div>
            <router-link :to="{name: 'policy_service_home', params: {id: service.id}}"
                         class="hover:underline">
              <span>{{ service.name }} - </span>
              <span class="italic">{{ service.description }}</span>
            </router-link>
          </div>
          <div class="grow"></div>
          <router-link :to="{name: 'policy_service_alignment', params: {id: service.id}}"
                       class="bg-yellow hover:bg-yellow-dark py-1 pl-4 pr-2 rounded">
            <span>View alignment</span>
            <VueFeather type="chevron-right" size="1.4rem" class="align-middle -mt-1"/>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {useAuth} from '@/store/auth'
import {storeToRefs} from 'pinia'
import {onMounted} from "vue";
import {api} from '@/utils/api'
import {ref} from 'vue'

const {institution} = storeToRefs(useAuth())
const services = ref([])

const getServices = async () => {
  services.value = await api.get('api/dissco/service')
}

onMounted(getServices)

</script>
