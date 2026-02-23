<script setup lang="ts">
import useMessage from '@/stores/message';

const { messages } = useMessage()
</script>

<template>
    <div style="position: absolute; right: 1rem; bottom: 0rem;" v-if="messages.length > 0">
        <p style="margin-bottom: 1rem;" v-for="message in messages">
            {{ message }}
        </p>
    </div>
</template>