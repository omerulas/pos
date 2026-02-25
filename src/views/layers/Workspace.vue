<script setup lang="ts">
import BackTablesButton from '@/component/buttons/BackTablesButton.vue';
import BrandButton from '@/component/buttons/BrandButton.vue';
import CheckInButton from '@/component/buttons/CheckInButton.vue';
import CheckOutButton from '@/component/buttons/CheckOutButton.vue';
import ConnectionStatus from '@/component/buttons/ConnectionStatus.vue';
import EnterOrder from '@/component/buttons/EnterOrder.vue';
import FullScreenButton from '@/component/buttons/FullScreenButton.vue';
import LogOutButton from '@/component/buttons/LogOutButton.vue';
import OrderHistory from '@/component/buttons/OrderHistory.vue';
import PrintBillButton from '@/component/buttons/PrintBillButton.vue';
import SyncButton from '@/component/buttons/SyncButton.vue';
import TableButton from '@/component/buttons/TableButton.vue';
</script>

<template>
    <header>
        <div style="display: flex; gap:0.25rem">
            <BrandButton />
            <ConnectionStatus />
            <TableButton />
        </div>
        <div style="display: flex; gap: 0.25rem">
            <CheckInButton />
            <PrintBillButton />
            <EnterOrder />
            <OrderHistory />
            <CheckOutButton />
            <FullScreenButton />
            <SyncButton />
            <BackTablesButton />
            <LogOutButton />
        </div>
    </header>
    <main>
        <router-view></router-view>
    </main>
</template>

<style scoped>
header {
    margin-bottom: 0.25rem;
    display: flex;
    justify-content: space-between;
    border-bottom: thin solid #ccc;
    padding-bottom: 0.5rem;
    margin-bottom: 0.5rem;
}

header button {
    height: 2.5rem;
}
</style>