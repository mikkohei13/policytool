<template>

  <div>
    <div class="text-4xl text-white font-bold pb-6">
      Create new maturity assessment team
    </div>
  </div>

  <div class="w-full border-2 bg-white p-4">
    <form class="flex flex-col gap-8 pl-2">
      <div class="text-lg prose max-w-none border-b-2 border-grey-light pb-2">
        Each digital maturity response is completed from the perspective of a team.
        Before you can start answering questions on behalf of the team, you need to tell us about
        them.
        The details entered below are only visible to you, so make them most useful to you!

        <p class="italic text-sm required text-status-denied pt-4">
          indicates required content
        </p>
      </div>

      <div class="flex flex-col gap-2">
        <label for="typeId" class="font-bold text-lg required">
          Who will you be completing the assessment primarily on behalf of?
        </label>
        <div v-if="'type' in errors">
          <p class="text-status-denied">
            Error: {{ errors['type'][0] }}
          </p>
        </div>
        <div id="typeId" class="flex flex-col">
          <div class="flex flex-row items-center gap-2">
            <input v-model="teamType" type="radio" id="type-team" value="team">
            <label for="type-team">A team or organisational unit within your organisation</label>
          </div>
          <div class="flex flex-row items-center gap-2">
            <input v-model="teamType" type="radio" id="type-organisation" value="organisation">
            <label for="type-organisation">Your whole organisation</label>
          </div>
          <div class="flex flex-row items-center gap-2">
            <input v-model="teamType" type="radio" id="type-node" value="node">
            <label for="type-node">A DiSSCo national node of one or more organisations</label>
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-2">
        <label for="nameId" class="font-bold text-lg required">
          Name
        </label>
        <div v-if="'name' in errors">
          <p class="text-status-denied">
            Error: {{ errors['name'][0] }}
          </p>
        </div>
        <input v-model="name" id="nameId" class="border rounded p-2" placeholder="Name">
      </div>

      <div class="flex flex-col gap-2">
        <label for="commentId" class="font-bold text-lg">
          Comments
        </label>
        <textarea v-model="comment" id="commentId" class="border rounded p-2" rows="4"
                  placeholder="Comment"></textarea>
      </div>
      <button
          class="bg-yellow rounded p-2 text-lg hover:bg-yellow-dark disabled:bg-grey disabled:cursor-not-allowed"
          @click.prevent="create" :disabled="!teamType || !name">
        Create team
      </button>
    </form>
  </div>
</template>

<script setup>

import {ref} from 'vue'
import {api} from '@/utils/api'
import {useRouter} from 'vue-router'

const router = useRouter()
const teamType = ref('')
const name = ref('')
const comment = ref('')
const errors = ref({})

const create = async () => {
  try {
    await api.post('/api/maturity/responder', {
      name: name.value,
      comment: comment.value,
      type: teamType.value
    })
    await router.push({name: 'maturity'})
  } catch (e) {
    const returnedErrors = e.response.data
    errors.value = {}
    for (const [field, error] of Object.entries(returnedErrors)) {
      errors.value[field] = error
    }
  }
}

</script>

<style scoped>
.required:before {
  content: " *";
  color: red;
  margin-right: 1px;
}
</style>