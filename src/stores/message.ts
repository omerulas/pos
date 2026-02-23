import { defineStore } from "pinia";
import { ref } from "vue";

const useMessage = defineStore('messageStore', () => {
    // --- States ---
    const messages = ref<string[]>([])

    // --- Methods ---
    function add(message: string) {
        messages.value.push(message)
        setTimeout(() => messages.value.pop(), 3000);
    }

    return {
        messages,
        add
    }
})

export default useMessage