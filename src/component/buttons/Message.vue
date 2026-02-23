<script setup lang="ts">
import useMessage from '@/stores/message';

const { messages } = useMessage()
</script>

<template>
    <div style="position: absolute; bottom: 0; right: 1rem; max-width: 15rem;" v-if="messages.length > 0">
        <div style="margin-bottom: 1rem;" v-for="message in messages">
            {{ message }}
        </div>
    </div>
</template>