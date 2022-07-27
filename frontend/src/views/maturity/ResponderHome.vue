<template>
  <div>
    <div class="text-4xl text-white font-bold pb-6">
      {{ responder?.name }} ({{ responder?.type }})
    </div>
  </div>

  <div class="flex flex-col lg:flex-row gap-8">
    <div class="w-full">
      <PackStatusList v-if="!!responder" type="maturity" title="Review Maturity Assessments"
                      :responderId="responder.id"></PackStatusList>
    </div>
  </div>
</template>

<script setup>
import PackStatusList from '@/components/packs/PackStatusList.vue'
import {api} from '@/utils/api'
import {onMounted, ref} from 'vue'

const {id} = defineProps(['id'])
const responder = ref(null)

const updateResponder = async () => {
  responder.value = await api.get(`/api/maturity/responder/${id}`)
}

onMounted(updateResponder)

</script>
