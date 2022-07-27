<template>
  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Maturity assessments
    </div>
  </div>

  <div class="flex flex-col lg:flex-row gap-8">
    <div class="w-full">
      <div class="border-2 bg-white p-3">
        <div class="flex flex-row gap-2 pb-3 border-b-2 border-black">
          <div class="text-black text-2xl">
            Your responses
          </div>
          <div class="grow"></div>
          <router-link :to="{name: 'maturity_create_team'}"
                       class="bg-yellow rounded py-1 pr-3 pl-1 hover:bg-yellow-dark text-lg">
            <VueFeather type="plus" size="1.4rem" class="align-middle mx-1 -mt-1"/>
            Create new team
          </router-link>
        </div>

        <template v-for="(respondents, type) in types">
          <div class="p-2 pt-4 border-b border-grey-dark text-xl flex flex-row">
            <VueFeather :type="typeIcons[type]" size="1.75rem"/>
            <span class="font-bold capitalize pl-2">{{ pluralize(type) }}</span>
          </div>
          <div class="flex flex-col gap-y-3 py-2">
            <template v-if="respondents.length === 0">
              <div class="pl-2 text-grey-dark">Your {{ type }} responses will appear here</div>
            </template>
            <template v-else>
              <div v-for="responder in respondents"
                   class="p-2 pl-2 hover:bg-grey-light text-lg flex flex-row items-center">
                <div class="pl-3">{{ responder.name }}</div>
                <div class="grow"/>
                <router-link
                    :to="{name: 'maturity_responder_home', params: {id: responder.id}}"
                    class="py-1 pl-4 pr-2 rounded bg-blue hover:bg-blue-dark">
                  View
                  <VueFeather type="chevron-right" size="1.4rem" class="align-middle -mt-1"/>
                </router-link>
              </div>
            </template>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import {api} from "@/utils/api";
import pluralize from 'pluralize'

const typeIcons = {
  team: 'users',
  organisation: 'layers',
  node: 'globe'
}
const types = ref({
  team: [],
  organisation: [],
  node: [],
})


const updateResponders = async () => {
  const responders = await api.get(`/api/maturity/responder`)
  for (const responder of responders) {
    types.value[responder.type].push(responder)
  }
}

onMounted(updateResponders)

</script>
