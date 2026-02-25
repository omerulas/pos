<script setup lang="ts">
import Messages from './component/Messages.vue';

</script>

<template>
  <router-view></router-view>
  <messages />
</template>

<style>
label{
  display: inline-block;
  width: 8rem;
}
form div {
  margin-bottom: 0.25rem;
}
table {
  width: 100%;
  border-collapse: collapse;
}

tr {
  text-align: left;
}

th,
td {
  padding: 8px;
  border: 1px solid #ddd;
  border-spacing: 0;
}

.actionButton {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
  height: 2.5rem;
}
</style>
