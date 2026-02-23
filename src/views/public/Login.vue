<script setup lang="ts">
import { initialCredentials } from '@/library/initials';
import { useProcess } from '@/stores/process';
import { ref } from 'vue';

const process = useProcess()

const credentials = ref({...initialCredentials})
</script>

<template>
    <h1>Giriş Yap</h1>
    <form @submit.prevent="process.login(credentials)">
        <div>
            <label>Kullanıcı Adı</label>
            <input v-model="credentials.username" type="text">
        </div>
        <div>
            <label>Şifre</label>
            <input v-model="credentials.password" type="password">
        </div>
        <button type="submit">Kaydet</button>
    </form>
</template>