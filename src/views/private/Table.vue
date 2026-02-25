<script setup lang="ts">
import AddToCartButton from '@/component/buttons/AddToCartButton.vue';
import CancelButton from '@/component/buttons/CancelButton.vue';
import DecreaseButton from '@/component/buttons/DecreaseButton.vue';
import EmptyCart from '@/component/buttons/EmptyCart.vue';
import IncreaseButton from '@/component/buttons/IncreaseButton.vue';
import PrintStatusButton from '@/component/buttons/PrintStatusButton.vue';
import RemoveButton from '@/component/buttons/RemoveButton.vue';
import SaveButton from '@/component/buttons/SaveButton.vue';
import { useOrderData } from '@/stores/order';
import { onMounted, onUnmounted } from 'vue';

const order = useOrderData()

onMounted(order.getOrder)
onUnmounted(order.reset)
</script>

<template>
    <section>
        <div>
            <div style="margin-bottom: 1rem;" v-if="$order.showOrderHistory">
                <div
                    style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <h2 style="padding: 0; margin: 0;">Sipariş Geçmişi</h2>
                    <div style="display: flex; gap: 0.25rem">
                        <CancelButton />
                    </div>
                </div>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th style="text-align: center; width: 1rem;">#</th>
                                <th>Ürün</th>
                                <th style="text-align: center; width: 8rem;">Adet</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="$order.cart.length > 0" v-for="(item, index) in $order.cart">
                                <td>{{ index + 1 }}</td>
                                <td>{{ item.name }}</td>
                                <td>
                                    <div
                                        style="display: flex; justify-content: start; gap: 0.25rem; flex: 0 0 auto; min-width: 0; flex-grow: 0;">
                                        <DecreaseButton :item-id="item.id" />
                                        <input style="width: 1.5rem; padding: 0.5rem 0 0.5rem 0.5rem;" type="number"
                                            v-model="item.quantity" disabled>
                                        <IncreaseButton :item-id="item.id" />
                                        <RemoveButton :item-id="item.id" />
                                    </div>
                                </td>
                            </tr>
                            <tr v-else>
                                <td colspan="3" style="text-align: center; padding: 1.2rem">
                                    Bu hesap için herhangi bir sipariş girilmemiş
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div style="margin-bottom: 1rem;" v-if="$order.canEnterOrder">
                <div
                    style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <h2 style="padding: 0; margin: 0;">Girilen Sipariş</h2>
                    <div style="display: flex; gap: 0.25rem">
                        <EmptyCart :disabled="$order.obj.id == '' || $order.cart.length == 0"/>
                        <SaveButton :disabled="$order.obj.id == '' || $order.cart.length == 0"></SaveButton>
                    </div>
                </div>
                <div>
                    <table>
                        <thead>
                            <tr>
                                <th style="text-align: center; width: 1rem;">#</th>
                                <th>Ürün</th>
                                <th style="text-align: center; width: 8rem;">Adet</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="$order.cart.length > 0" v-for="(item, index) in $order.cart">
                                <td>{{ index + 1 }}</td>
                                <td>{{ item.name }}</td>
                                <td>
                                    <div
                                        style="display: flex; justify-content: start; gap: 0.25rem; flex: 0 0 auto; min-width: 0; flex-grow: 0;">
                                        <DecreaseButton :item-id="item.id" />
                                        <input style="width: 1.5rem; padding: 0.5rem 0 0.5rem 0.5rem;" type="number"
                                            v-model="item.quantity" disabled>
                                        <IncreaseButton :item-id="item.id" />
                                        <RemoveButton :item-id="item.id" />
                                    </div>
                                </td>
                            </tr>
                            <tr v-else>
                                <td colspan="3" style="text-align: center; padding: 1.2rem">
                                    Sipariş kalemi girilmemiş
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div>
                <div
                    style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.25rem;">
                    <h2 style="padding: 0; margin: 0;">Tüm Siparişler</h2>
                    <PrintStatusButton />
                </div>
                <table>
                    <thead>
                        <tr>
                            <th style="text-align: center; width: 1rem;">#</th>
                            <th>Ürün</th>
                            <th style="text-align: center; width: 5rem;">Birim Fiyat</th>
                            <th style="text-align: center; width: 5rem;">Adet</th>
                            <th style="text-align: center; width: 5rem;">Tutar</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-if="$order.obj.items.length > 0" v-for="(item, index) in $order.obj.items">
                            <td>{{ index + 1 }}</td>
                            <td>{{ item.name }}</td>
                            <td style="text-align: right;">{{ item.unit_price }} ₺</td>
                            <td style="text-align: center;">{{ item.quantity }}</td>
                            <td style="text-align: right;">{{ item.amount }} ₺</td>
                        </tr>
                        <tr v-if="$order.obj.items.length > 0">
                            <td style="padding: 16px 8px;" colspan="4">
                                <strong>Toplam</strong>
                            </td>
                            <td style="text-align: right;">
                                <strong>{{ $order.obj.amount }} ₺</strong>
                            </td>
                        </tr>
                        <tr v-else>
                            <td colspan="5" style="text-align: center; padding: 1.2rem;">
                                Bu masaya henüz bir sipariş girilmemiş
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <aside>
            <div style="height: 2.5rem; display: flex; gap: 0.25rem; margin-bottom: 0.25rem;">
                <button :disabled="!$order.canEnterOrder" v-for="category in $process.store.categories" @click="$order.changeCategoryId(category.id)">
                    {{ category.name }}
                </button>
            </div>

            <table>
                <thead>
                    <tr>
                        <th style="width: 2rem;">#</th>
                        <th>Ürün</th>
                        <th style="width: 5rem;">Eylem</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(product, index) in $order.categoryProducts" :key="product.id">
                        <td>{{ index + 1 }}</td>
                        <td>{{ product.name }}</td>
                        <td>
                            <AddToCartButton :disabled="$order.obj.id == ''" :product-id="product.id" />
                        </td>
                    </tr>
                    <tr v-if="$order.selectedCategoryId == ''">
                        <td colspan="3" style="text-align: center; padding: 1.20rem 0;">Ürün eklemek için kategori
                            seçiniz</td>
                    </tr>
                </tbody>
            </table>
        </aside>
    </section>
</template>

<style scoped>
section {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.25rem;
    width: 100%;
    margin-bottom: 0.5rem;
}
</style>
