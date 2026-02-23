import { api } from "@/library/api";
import { initialStore } from "@/library/initials";
import type { LoginCredentials, Response, Store } from "@/library/interface";
import { urls } from "@/library/urls";
import { defineStore } from "pinia";
import { ref } from "vue";
import { useRouter } from "vue-router";

export const useProcess = defineStore("Process", () => {
  // --- Stores ---
  const router = useRouter();
  const process = useProcess();

  // --- States ---
  const isChecked = ref(false);
  const isLoading = ref(false);
  const isAuthenticated = ref(false);
  const store = ref<Store>({ ...initialStore });

  // --- Functions ---
  function set(response: Response) {
    isChecked.value = true;
    isAuthenticated.value = response.data.is_authenticated;
    store.value = response.data.store;
  }

  async function check() {
    const response = await api.get(urls.check);
    if (response.status == 200) {
      set(response);
    }
  }

  async function login(credentials: LoginCredentials) {
    const response = await api.post(urls.login, credentials);
    if (response.status == 200) {
      set(response);
      router.push({ name: "workspace" });
    }
  }

  async function logout() {
    const response = await api.delete(urls.logout);
    process.isAuthenticated = response.data.is_authenticated;
    router.push({ name: "login" });
  }

  return {
    isChecked,
    isAuthenticated,
    isLoading,
    store,
    login,
    check,
    logout,
  };
});
