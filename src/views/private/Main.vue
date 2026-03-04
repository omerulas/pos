<template>
    <div>
        <button @click="$router.push({
            name: 'table',
            params: { id: table.id }
        })" v-for="table in $process.store.tables" :style="!table.available ? 'background-color: coral;' : ''">
            {{ table.name }}
        </button>
    </div>
</template>

<style scoped>
div {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.25rem;
    grid-column: span 3;
}

button {
    width: 100%;
    height: 13rem;
}
</style>