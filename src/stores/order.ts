import { defineStore } from "pinia";
import { computed, ref, watch } from "vue";
import { useProcess } from "./process";
import { useRoute } from "vue-router";
import type { CartItem, Order } from "@/library/interface";
import { initialOrder } from "@/library/initials";
import { api } from "@/library/api";
import { url, urls } from "@/library/urls";
import useMessage from "./message";

export const useOrderData = defineStore("Order", () => {
  // --- Stores ---
  const route = useRoute();
  const process = useProcess();
  const message = useMessage();

  // --- States ---
  const selectedCategoryId = ref<string>("");
  const cart = ref<CartItem[]>([]);
  const obj = ref<Order>({ ...initialOrder });
  const canEnterOrder = ref(false)
  const showOrderHistory = ref(false)

  // --- Computeds ---
  const tableId = computed(() => route.params.id);

  const table = computed(() => {
    return process.store.tables.find((table) => {
      return table.id == tableId.value || null;
    });
  });

  const categoryProducts = computed(() => {
    if (!process.store.categories) return [];

    const category = process.store.categories.find(
      (cat) => cat.id === selectedCategoryId.value,
    );

    return category ? category.products : [];
  });

  // --- Functions ---
  function changeCategoryId(id: string) {
    selectedCategoryId.value = id;
  }

  async function getOrder() {
    const response = await api.get(url({ path: `order/${tableId.value}` }));
    if (response.status == 200) {
      obj.value = response.data;
    }
  }

  async function openOrder() {
    if (obj.value.id !== "") return;

    const response = await api.post(urls.order, { table: tableId.value });

    if (response.status == 200) {
      obj.value = response.data;
    }
  }

  function addToCart(productId: string) {
    const categoryList = process.store.categories;
    const product = categoryList
      .flatMap((category) => category.products)
      .find((p) => p.id === productId);

    if (product) {
      const existingCartItem = cart.value.find(
        (item) => item.product === productId,
      );

      if (existingCartItem) {
        message.add("Bu ürün zaten mevcut, miktarını güncelleyiniz");
      } else {
        cart.value.push({
          id: crypto.randomUUID(),
          order: obj.value.id,
          product: product.id,
          name: product.name,
          quantity: 1,
        });
      }
    }
  }

  function increaseQuantity(itemId: string) {
    const item = cart.value.find((item) => item.id == itemId);

    if (item) {
      item.quantity++;
    }
  }

  function decreaseQuantity(itemId: string) {
    const item = cart.value.find((item) => item.id == itemId);

    if (item && item.quantity > 1) {
      item.quantity--;
    }
  }

  function removeItem(itemId: string) {
    const conf = window.confirm("Ürün tamamen kaldırılacak");

    if (conf) {
      cart.value = cart.value.filter((item) => item.id != itemId);
    }
  }

  async function saveOrder() {
    if (cart.value.length == 0) return;

    const response = await api.put(urls.order, {
      order: obj.value.id,
      items: cart.value,
    });

    if (response.status == 200) {
      obj.value = response.data;
      cart.value = []
    }
  }

  async function cancelTicket(ticketId: string) {
    const conf = window.confirm("Tüm istem iptal edilecek")

    if(conf){
      console.log(ticketId)
      const response = await api.delete(url({path: `ticket/${ticketId}`}))

      if(response.status == 200) {
        obj.value = response.data
      }
    }
  }

  function reset() {
    obj.value = { ...initialOrder };
    selectedCategoryId.value = "";
    canEnterOrder.value = false;
    showOrderHistory.value = false;
  }

  return {
    categoryProducts,
    selectedCategoryId,
    tableId,
    table,
    cart,
    obj,
    canEnterOrder,
    showOrderHistory,
    changeCategoryId,
    getOrder,
    openOrder,
    addToCart,
    increaseQuantity,
    decreaseQuantity,
    removeItem,
    saveOrder,
    cancelTicket,
    reset,
  };
});
