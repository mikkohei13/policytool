<template>
  <div class="flex flex-row items-center p-2 hover:bg-grey-light">
    <div>
      <span>{{ pack.name }} - </span>
      <span class="italic">{{ pack.size }} questions</span>
    </div>
    <div class="grow"></div>
    <router-link
        :to="{name: 'pack', params: {id: pack.id, type: pack.type, responderId: pack.responder_id}}"
        :class="statusOption.class" class="py-1 pl-4 pr-2 rounded">
      {{ statusOption.text }}
      <VueFeather type="chevron-right" size="1.4rem" class="align-middle -mt-1"/>
    </router-link>
  </div>
</template>

<script setup>

</script>
