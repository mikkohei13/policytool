<template>

  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Create new institution policy entry
    </div>
  </div>

  <div class="w-full border-2 bg-white p-4">
    <form class="flex flex-col gap-8 pl-2">
      <div class="text-lg prose max-w-none border-b-2 border-grey-light pb-2">
        some intro text needed...

        <p class="italic text-sm required text-status-denied pt-4">
          indicates required content
        </p>
      </div>

      <div class="flex flex-col gap-2">
        <label for="nameId" class="font-bold text-lg required">
          Policy entry name
        </label>
        <FormError :errors="errors" field="name"></FormError>
        <input v-model="name" id="nameId" class="border rounded p-2">
      </div>

      <div class="flex flex-col gap-2">
        <label for="statusId" class="font-bold text-lg required">
          Policy status
        </label>
        <div class="italic text-sm">
          Whether the institution has a formally documented policy, undocumented procedure, or
          nothing at all
        </div>
        <FormError :errors="errors" field="status"></FormError>
        <div id="statusId" class="flex flex-col">
          <div class="flex flex-row items-center gap-2">
            <input v-model="status" type="radio" id="status-documented" value="documented">
            <label for="status-documented">Documented</label>
          </div>
          <div class="flex flex-row items-center gap-2">
            <input v-model="status" type="radio" id="status-undocumented" value="undocumented">
            <label for="status-undocumented">Undocumented</label>
          </div>
          <div class="flex flex-row items-center gap-2">
            <input v-model="status" type="radio" id="status-not-in-place" value="not_in_place">
            <label for="status-not-in-place">Not in place</label>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-2">
        <label for="documentationDateId" class="font-bold text-lg">
          Documentation date
        </label>
        <div class="italic text-sm">Date that the document was written</div>
        <FormError :errors="errors" field="documentation_date"></FormError>
        <Datepicker id="documentationDateId" v-model="documentationDate" :enableTimePicker="false"
                    format="dd-MM-yyyy" autoApply/>
      </div>

      <div class="flex flex-col gap-2">
        <label for="documentationNextReviewDateId" class="font-bold text-lg">
          Next documentation review date
        </label>
        <div class="italic text-sm">Date that the documentation is next due to be reviewed</div>
        <FormError :errors="errors" field="documentation_next_review_date"></FormError>
        <Datepicker id="documentationNextReviewDateId" v-model="documentationNextReviewDate"
                    :enableTimePicker="false" format="dd-MM-yyyy" autoApply/>
      </div>

      <div class="flex flex-col gap-2">
        <label for="documentationPublicId" class="font-bold text-lg">
          Is the documentation publicly available?
        </label>
        <div class="italic text-sm">
          Whether the documentation is public or has been released for internal use only
        </div>
        <FormError :errors="errors" field="documentation_public"></FormError>
        <div id="documentationPublicId" class="flex flex-col">
          <div class="flex flex-row items-center gap-2">
            <input v-model="documentationPublic" type="radio" id="public-internal" value="internal">
            <label for="public-internal">Internal</label>
          </div>
          <div class="flex flex-row items-center gap-2">
            <input v-model="documentationPublic" type="radio" id="public-public" value="public">
            <label for="public-public">Public</label>
          </div>
          <div class="flex flex-row items-center gap-2">
            <input v-model="documentationPublic" type="radio" id="public-partly-public"
                   value="partly_public">
            <label for="public-partly-public">Partly public</label>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-2">
        <label for="documentationShareableId" class="font-bold text-lg">
          Is the documentation shareable?
        </label>
        <div class="italic text-sm">
          Whether the institution is willing and able to openly share the policy documentation
        </div>
        <FormError :errors="errors" field="documentation_shareable"></FormError>
        <div id="documentationShareableId" class="flex flex-col">
          <div class="flex flex-row items-center gap-2">
            <input v-model="documentationShareable" type="radio" id="share-dissco" value="dissco">
            <label for="share-dissco">DiSSCo partners only</label>
          </div>
          <div class="flex flex-row items-center gap-2">
            <input v-model="documentationShareable" type="radio" id="share-public" value="public">
            <label for="share-public">Public</label>
          </div>
          <div class="flex flex-row items-center gap-2">
            <input v-model="documentationShareable" type="radio" id="share-unsure"
                   value="no_unsure">
            <label for="share-unsure">No, unsure</label>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-2">
        <label for="documentationDetailsId" class="font-bold text-lg required">
          Details of the policy documentation
        </label>
        <div class="italic text-sm">
          Details of the policy documents themselves.
          This could include links to online documentation and details of the relevant sections
          within the documentation if required.
        </div>
        <FormError :errors="errors" field="documentation_details"></FormError>
        <textarea v-model="documentationDetails" id="documentationDetailsId" rows="4"></textarea>
      </div>

      <div class="flex flex-col gap-2">
        <label for="policySummaryId" class="font-bold text-lg">
          A summary of the policy document if it isn't available or can't be shared
        </label>
        <FormError :errors="errors" field="policy_summary"></FormError>
        <textarea v-model="policySummary" id="policySummaryId" rows="4"></textarea>
      </div>

      <div class="flex flex-col gap-2">
        <label for="additionalNotesId" class="font-bold text-lg">
          Any additional notes relevant to the information or its use
        </label>
        <FormError :errors="errors" field="additional_notes"></FormError>
        <textarea v-model="additionalNotes" id="additionalNotesId" rows="4"></textarea>
      </div>

      <div class="flex flex-col gap-2">
        <label for="policyAreaId" class="font-bold text-lg">
          Select the policy area this policy applies to
        </label>
        <FormError :errors="errors" field="policy_area"></FormError>
        <select v-model="policyArea" id="policyAreaId">
          <option v-for="area in policyAreas" :value="area.id">
            {{ area.name }}
          </option>
        </select>
      </div>

      <button
          class="bg-yellow rounded p-2 text-lg hover:bg-yellow-dark disabled:bg-grey disabled:cursor-not-allowed"
          @click.prevent="create" :disabled="!createButtonEnabled()">
        Create policy
      </button>
    </form>
  </div>
</template>

<script setup>

import FormError from '@/components/forms/FormError.vue'
import {onMounted, ref} from 'vue'
import {api} from '@/utils/api'
import {useRouter} from 'vue-router'
import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

const router = useRouter()

const name = ref('')
const status = ref('')
const documentationDate = ref('')
const documentationNextReviewDate = ref('')
const documentationPublic = ref('')
const documentationShareable = ref('')
const documentationDetails = ref('')
const policySummary = ref('')
const additionalNotes = ref('')
const policyArea = ref(null)

const errors = ref({})
const required = [status, documentationDetails]
const policyAreas = ref([])

const create = async () => {
  try {
    await api.post('api/policy/', {
      name: name.value,
      status: status.value,
      documentation_date: documentationDate.value || null,
      documentation_next_review_date: documentationNextReviewDate.value || null,
      documentation_public: documentationPublic.value,
      documentation_shareable: documentationShareable.value,
      documentation_details: documentationDetails.value,
      policy_summary: policySummary.value,
      additional_notes: additionalNotes.value,
      policy_area: policyArea.value
    })
    await router.push({name: 'policy_docs'})
  } catch (e) {
    const returnedErrors = e.response.data
    errors.value = {}
    for (const [field, error] of Object.entries(returnedErrors)) {
      errors.value[field] = error
    }
  }
}

const createButtonEnabled = () => required.every(field => !!field.value)


const getOptions = async () => {
  policyAreas.value = await api.get('api/dissco/policy/')
}

onMounted(getOptions)

</script>

<style scoped>
.required:before {
  content: " *";
  color: red;
  margin-right: 1px;
}
</style>