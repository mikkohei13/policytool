<template>

  <div class="border-2 bg-white p-3">
    <div class="flex flex-row gap-2 pb-3 border-b-2 border-black">
      <div class="text-black text-3xl">
        Institutional Policies
      </div>
      <div class="grow"></div>
      <router-link :to="{name: 'policy_create_doc'}"
                   class="bg-yellow rounded py-1 pr-3 pl-1 hover:bg-yellow-dark text-lg">
        <VueFeather type="plus" size="1.4rem" class="align-middle mx-1 -mt-1"/>
        Add policy
      </router-link>
    </div>

    <div class="flex flex-col pt-4">
      <div v-for="policy in policies" class="border-b-2 first:border-t-2 border-grey p-4 hover:bg-grey-lighter">
        <div class="text-2xl capitalize underline">{{ policy.name }}</div>
        <div class="flex flex-row gap-6">
          <Markdown class="basis-3/5 text-base"
                    :markdown="policy.documentation_details || policy.policy_summary"></Markdown>
          <div class="basis-2/5 flex flex-col">
            <div><span class="font-bold">Status: </span><span class="italic">{{
                policy.status
              }}</span></div>
            <div v-for="optional in optionalFields">
              <template v-if="!!policy[optional.field]">
                <span class="font-bold">{{ optional.label }}: </span>
                <span class="italic">{{ policy[optional.field] }}</span>
              </template>
            </div>
            <div v-if="policy.policy_area in disscoPolicies">
              <span class="font-bold">Policy area: </span>
              <!-- this should be a link to the policy -->
              <span class="italic">{{ disscoPolicies[policy.policy_area].name }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import {api} from "@/utils/api"
import Markdown from '@/components/Markdown.vue'

const policies = ref([])
const disscoPolicies = ref({})

const optionalFields = [
  {field: 'documentation_date', label: 'Documentation creation date'},
  {field: 'documentation_next_review_date', label: 'Next documentation review date'},
  {field: 'documentation_public', label: 'Is public'},
  {field: 'documentation_shareable', label: 'Shareable'},
  {field: 'additional_notes', label: 'Additional notes'},
]

const updatePolicies = async () => {
  policies.value = await api.get(`api/policy/`)

  const disscoPoliciesArray = await api.get('api/dissco/policy/')
  disscoPoliciesArray.forEach(disscoPolicy => {
    disscoPolicies.value[disscoPolicy.id] = disscoPolicy
  })
}

onMounted(updatePolicies)

</script>
